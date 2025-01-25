import json
import re
import sys
import typing as t
from glob import glob
from pathlib import Path
from shutil import copy, rmtree

import frontmatter
import typer
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from slugify import slugify

app = typer.Typer()


class LinkConfig(t.TypedDict):
    text: str
    link: str
    collapsed: t.NotRequired[bool]
    items: t.NotRequired[list["LinkConfig"]]


FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".svg", ".md"]


class Processor:
    def __init__(
        self,
        base_dir: Path,
        source_dir: Path,
        template_dir: Path,
        target_dir: str,
        ignored_dirs: [str],
        format: bool,
    ) -> None:
        self.base_dir = base_dir
        self.source_dir = source_dir
        self.template_dir = template_dir
        self.target_dir = base_dir / target_dir
        self.ignored_dirs = ignored_dirs
        self.format = format

    def process(self):
        # Copy source files
        logger.info("Copying sources files")
        self.copy_files(
            self.source_dir,
            self.target_dir,
            ignored_dirs=self.ignored_dirs,
        )

        logger.info("Cleaning filenames")
        self.clean_filenames(self.target_dir)

        logger.info("Generating links.json config file")
        self.generate_links_config(self.target_dir)

        # Add index files in folders
        logger.info("Adding index.md files to folders")
        self.add_index_files(self.target_dir)

        # Add title of files in frontmatter of Markdownfiles
        logger.info("Adding title of files to frontmatters")
        self.add_frontmatter_titles(self.target_dir)

        # Slugify all folders and files
        logger.info("Slugifying folders and files names")
        self.slugify_dirs(self.target_dir)

        if self.format:
            logger.info("Processing markdown of files")
            self.process_markdown_files(self.target_dir)

    def clean_filenames(self, dir: Path):
        for child in dir.iterdir():
            if match := re.match(r"^\d+\s?[.-]\s?(.*?)$", child.name):
                logger.debug(f"Moving {child} to {child.parent/match[1]}")
                child.rename(child.parent / match[1])
            if child.is_dir():
                self.clean_filenames(child)

    def relative_link(self, path: str | Path, relative: Path = None):
        path = Path(path)
        return path.relative_to(relative or self.base_dir)

    def copy_files(self, dir_src: Path, dir_target: Path, ignored_dirs: [str] = []):
        # Delete the source dir first
        if dir_target.exists():
            logger.debug("Cleaning target dir")
            rmtree(dir_target)

        # Copy all files and subdirs from the src dir to the target, while ignoring the specified dirs.
        dir_target.mkdir(parents=True, exist_ok=True)
        logger.debug(
            f"Copying files from {self.relative_link(dir_src, self.source_dir)}"
        )
        for path in dir_src.iterdir():
            if path.is_dir():
                if path.name in ignored_dirs:
                    logger.debug(
                        f"Ignoring dir {path.name} (found in list of ignored dirs: {ignored_dirs})"
                    )
                    continue
                if (path / ".hide").exists():
                    logger.debug(
                        f"Ignoring dir {path.name} (found file {(path / '.hide')})"
                    )
                    continue
                self.copy_files(path, dir_target / path.name)
            else:
                copy(path, dir_target / path.name)

    def add_frontmatter_title(self, file: Path):
        with open(file) as f:
            post = frontmatter.load(f)
        if not post.metadata.get("title"):
            if file.name == "index.md":
                # With an index.md file, the title is the name of the folder, before being sluggified
                title = file.parts[-2]
            else:
                title = file.stem
            logger.debug(
                f'Adding title "{title}" to "{self.relative_link(file, self.target_dir)}"'
            )
            post.metadata["title"] = title
            with open(file, "w") as f:
                f.write(frontmatter.dumps(post))

    def add_frontmatter_titles(self, dir_src: Path):
        for item in dir_src.iterdir():
            if item.is_dir():
                self.add_frontmatter_titles(item)
            elif item.suffix == ".md":
                self.add_frontmatter_title(item)

    def slugify_path(self, path: Path) -> Path:
        if path.is_dir():
            name = slugify(path.name)
        else:
            name = slugify(path.stem) + (f"{path.suffix}" if path.suffix else "")
        new_path = path.parent / name
        path.rename(new_path)
        return new_path

    def slugify_dirs(self, dir_src: Path):
        # Slugify all folders and files in a directory.
        # Recursively calls itself for nested directories
        dirs, files = [], []
        for item in dir_src.iterdir():
            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)
        for dir in dirs:
            new_dir = self.slugify_path(dir)
            self.slugify_dirs(new_dir)
        for file in files:
            self.slugify_path(file)

    def add_index_files(self, dir_src: Path):
        # Add index.md file to directories which don't have one
        dirs, files = [], []
        for item in dir_src.iterdir():
            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)
        for dir in dirs:
            self.add_index_files(dir)
        if not any([item.name == "index.md" for item in files]):
            if dir_src == self.target_dir:
                template_file = "root-index.md.j2"
            else:
                template_file = "index.md.j2"
            logger.debug(
                f"Adding index file in {self.relative_link(dir_src, self.target_dir)}, using {template_file}"
            )
            copy(self.template_dir / template_file, dir_src / "index.md")
        else:
            logger.debug(
                f"Index file already exists in {self.relative_link(dir_src, self.target_dir)}, skipping"
            )

    def generate_links_config(self, dir_src: Path):
        def generate_links_config_of_item(item: Path, index: int) -> LinkConfig:
            if item.is_file():
                link = Path(item).relative_to(dir_src)
                parts = list(link.parts)
                parts[-1] = parts[-1].replace(".md", "")
                return {
                    "text": item.stem,
                    "link": "/" + "/".join([slugify(p) for p in parts]),
                }

            child_items: list[LinkConfig] = []
            for child in item.iterdir():
                if child.is_file() and not child.name.endswith("md"):
                    continue
                child_config = generate_links_config_of_item(child, index=index + 1)
                if "collapsed" in child_config.keys():
                    if child_config.get("items"):
                        # Dir with not empty list of childs
                        child_items.append(child_config)
                else:
                    child_items.append(child_config)
            item_config: LinkConfig = {
                "text": item.name,
                "link": (
                    "/"
                    + "/".join(
                        [slugify(p) for p in Path(item).relative_to(dir_src).parts]
                    )
                    + "/"
                ),
                "collapsed": bool(index > 0),
            }
            if child_items:
                item_config["items"] = sorted(
                    child_items, key=lambda item: item["text"]
                )
            return item_config

        config: list[LinkConfig] = []
        for child in dir_src.iterdir():
            if child.is_file() and not child.name.endswith("md"):
                continue
            child_config = generate_links_config_of_item(child, index=0)
            if "collapsed" in child_config.keys():
                if child_config.get("items"):
                    # Dir with not empty list of childs
                    config.append(child_config)
            else:
                config.append(child_config)
        config = sorted(config, key=lambda item: item["text"])

        with open(dir_src / "links.json", "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def locate_file(self, filename: str) -> str:
        files = [
            Path(f)
            for f in glob(str(self.target_dir / f"**/{filename}*"), recursive=True)
        ]
        files = [f for f in files if f.is_file()]
        logger.debug(
            f"Found {[str(f) for f in files] if files else 'no match'} for {filename}"
        )
        if files:
            return str(files[0].relative_to(self.target_dir))
        return ""

    def process_links(self, content: str, filepath: Path | str) -> str:
        r = r"\[\[(.*?)\]\]"
        # This offset is used to account for the change of length
        # in the link's length before and after the change of format.
        offset = 0
        for m in re.finditer(r, content):
            start = m.start(0) + offset
            end = m.end(0) + offset
            link = m[1]
            title = ""
            if link.find("|") > 0:
                link, title = link.split("|", 1)
                link = link.strip()
                title = title.strip()
            link_id = ""
            if link.find("#") > 0:
                parts = link.split("#", 1)
                link = parts[0]
                link_id = parts[1]
            file_extension = ""
            for extension in FILE_EXTENSIONS:
                if link.endswith(extension):
                    link = link[: len(link) - len(extension)]
                    file_extension = extension
            link = "/".join([slugify(p) for p in link.split("/")]) + file_extension
            link = self.locate_file(filename=link)
            if link_id:
                link = f"{link}#{link_id}"
            logger.debug(f'Processing link "{link}" ({filepath})')
            formatted_link = f"[{title}](/{link})"
            if start >= 1 and content[start - 1] == "!":
                formatted_link = f"!{formatted_link}"
            content = content[:start] + formatted_link + content[end:]
            original_lenght = len(m[0])
            new_length = len(formatted_link)
            offset += new_length - original_lenght
        return content

    def process_citations(self, content: str, *_: t.Any) -> str:
        if content.find(">") == -1:
            # No citation block found in the file, no need to go any further.
            return content

        lines = content.split("\n")
        citations: list[tuple[int, int]] = []
        start, end = -1, -1
        index = 0
        # Locate the index of the beginning and end of the citations blocks
        # so that they can be properly formatted as a whote afterwards.
        for index, line in enumerate(lines):
            if not line or line[0] != ">":
                if start >= 0:
                    end = index
                    citations.append((start, end))
                    start, end = -1, -1
                continue
            if start < 0:
                start = index
        offset = 0
        for start, end in citations:
            cited_lines = [
                l.lstrip(">")[1:] for l in lines[start + offset : end + offset]
            ]
            for src, dst in [
                ("note", "info"),
                ("warning", "warning"),
            ]:
                if cited_lines[0].startswith(f"[!{src}]"):
                    cited_lines[0] = f"::: {dst}" + cited_lines[0][(len(f"[!{src}]")) :]
                    break
            cited_lines.append(":::")
            lines = lines[: start + offset] + cited_lines + lines[end + offset :]
            offset += 1
        return "\n".join(lines)

    def process_headers(self, content: str, filepath: Path | str) -> str:
        if content.find("#") == -1:
            # No headers in the file, no need to go any further
            return content

        if filepath.name == "index.md":
            return content

        lines = content.split("\n")
        for index, line in enumerate(lines):
            vals = line.split()
            if vals and (val := vals[0]) and val.startswith("#"):
                lines[index] = f"#{line}"
        return "\n".join(lines)

    def process_markdown_file(self, file: Path):
        with open(file) as f:
            post = frontmatter.load(f)
        content = post.content

        for f in [
            self.process_links,
            self.process_citations,
            self.process_headers,
        ]:
            content = f(content, file)

        if file.name != "index.md":
            # Use base template for all files except for index files which have their own templates
            environment = Environment(loader=FileSystemLoader(self.template_dir))
            template = environment.get_template("base.md.j2")
            content = template.render(content=content)

        post.content = content
        with open(file, "w") as f:
            f.write(frontmatter.dumps(post))

    def process_markdown_files(self, dir: Path):
        for child in dir.iterdir():
            if child.is_file() and child.suffix == ".md":
                self.process_markdown_file(child)
            elif child.is_dir():
                self.process_markdown_files(child)


def main(
    target_dir: t.Optional[str] = "./build",
    source_dir: t.Optional[str] = "./sources",
    base_dir: t.Optional[str] = ".",
    template_dir: t.Optional[str] = "./templates",
    ignored_dirs: t.Optional[str] = "",
    format: t.Optional[bool] = True,
    verbose: t.Optional[bool] = False,
):
    source_dir = Path(source_dir).resolve()
    base_dir = Path(base_dir).resolve()
    template_dir = Path(template_dir).resolve()
    ignored_dirs = [dir.strip() for dir in ignored_dirs.split(",") if dir]

    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> <level>{message}</level>",
        colorize=True,
    )
    if verbose:
        logger.add(
            sys.stdout,
            level="DEBUG",
            format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> {message}",
            colorize=True,
            filter=lambda record: record["level"].no < 20,
        )

    processor = Processor(
        base_dir=base_dir,
        source_dir=source_dir,
        target_dir=target_dir,
        template_dir=template_dir,
        ignored_dirs=ignored_dirs,
        format=format,
    )
    processor.process()


if __name__ == "__main__":
    typer.run(main)
