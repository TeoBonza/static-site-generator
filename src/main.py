import os
import sys
import shutil
from textnode import markdown_to_html_node, extract_title

def copy_directory(src_path, dest_path):
    """
    Recursively copy all contents from src_path to dest_path.
    """
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        print(f"Created directory: {dest_path}")

    # Iterate through all items in the source directory
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)
            print(f"Copied file: {src_item} -> {dest_item}")
        else:
            # Recursively copy subdirectory
            copy_directory(src_item, dest_item)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from a markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, "r") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # Replace root paths with basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    # Create destination directory if needed
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Write the output file
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from all markdown files in a directory.
    """
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path):
            # Convert .md files to .html
            if item.endswith(".md"):
                dest_file = item[:-3] + ".html"
                dest_path = os.path.join(dest_dir_path, dest_file)
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            # Recursively process subdirectories
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir, basepath)

def main():
    # Get basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Delete docs directory if it exists to ensure clean copy
    if os.path.exists("docs"):
        shutil.rmtree("docs")
        print("Deleted existing docs directory")

    # Copy static to docs
    copy_directory("static", "docs")

    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
