from bs4 import NavigableString
from ..transformers.image_transformer import ImageTransformer

class BaseConverter:
    def __init__(self):
        pass

    def convert_inline_content(self, node):
        """Convierte contenido inline como texto, negritas, cursivas y enlaces."""
        if isinstance(node, NavigableString):
            return {"text": str(node).strip(), "type": "text"} if str(node).strip() else None
        elif node.name in ['b', 'strong']:
            return {"bold": True, "text": f" {node.get_text().strip()} ", "type": "text"}
        elif node.name in ['i', 'em']:
            return {"italic": True, "text": f" {node.get_text().strip()} ", "type": "text"}
        elif node.name == 'a':
            href = node.get('href', '')
            text = node.get_text().strip() or "Link"
            return {
                "type": "link",
                "url": href,
                "children": [{"text": f" {text} ", "type": "text"}]
            }
        else:
            return {"text": node.get_text().strip(), "type": "text"}

    def convert_node_to_block(self, node, images_info, image_transformer: ImageTransformer):
        """Convierte un nodo HTML a un bloque JSON."""
        if node.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(node.name[1])
            return {
                "type": "heading",
                "children": [{"text": node.get_text().strip(), "type": "text"}],
                "level": level,
                "size": f"h{level}"
            }
        elif node.name == 'p':
            children = []
            for child in node.children:
                content = self.convert_inline_content(child)
                if content:
                    children.append(content)
            return {"type": "paragraph", "children": children} if children else None
        elif node.name in ['ul', 'ol']:
            list_type = "unordered" if node.name == 'ul' else "ordered"
            children = []
            for li in node.find_all('li', recursive=False):
                li_children = [content for child in li.children if (content := self.convert_inline_content(child))]
                if li_children:
                    children.append({
                        "type": "list-item",
                        "children": li_children
                    })
            return {
                "type": "list",
                "format": list_type,
                "children": children
            } if children else None
        elif node.name == 'img':
            return image_transformer.transform_image(node, images_info)
        return None

    def convert_html_to_json_blocks(self, soup, images_info, image_transformer: ImageTransformer):
        """Convierte todo el HTML a una lista de bloques JSON."""
        blocks = []
        for node in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'img']):
            block = self.convert_node_to_block(node, images_info, image_transformer)
            if block:
                blocks.append(block)
        return blocks
