from lxml import etree

# consts
ROOT_ELEMENT = "queries"

# dataclasses
class Query:
    def __init__(self, q_id):
        self.qtext = ""
        self.constraint_groups = []
        self.id = q_id

class ConstraintGroup:
    def __init__(self, relation="and"):
        self.bool_relation = relation
        self.constraints = []

class Constraint:
    def __init__(self):
        self.type = "text"
        self.relation = "in"
        self.key = ""
        self.value = ""


def load_file(file_path):
    with open(file_path, "r") as FILE:
        tree = etree.parse(FILE)
        root = tree.getroot()
        last_query = root.xpath("//query[last()]")
        if last_query is not None:
            last_query_id = int(last_query[0].attrib["id"])
        else:
            last_query_id = 0

        return (tree, root, last_query_id)

def get_new_file():
    root = etree.Element(ROOT_ELEMENT)
    tree = etree.ElementTree(root)
    last_query_id = 0

    return (tree, root, last_query_id)

def init_file(root_path, dest_folder, name):
    file_path = f"{root_path}{dest_folder}{name}.xml"

    try:
        etree, root, last_query_id = load_file(file_path)
    except (FileNotFoundError, IOError) as e:
        etree, root, last_query_id = get_new_file()

    return (etree, root, last_query_id)

def add_new_query(etree, root, query):
    new_query = etree.SubElement(root, "query")
    new_query.set("id", str(query.id))
    new_qtext = etree.SubElement(new_query, "qtext")
    new_qtext.text = query.qtext
    new_constraints = etree.SubElement(new_query, "constraints")
    
    for group in query.constraint_groups:
        new_group = etree.SubElement(new_constraints, "group")
        new_group.set("bool-relation", group.bool_relation)
        for constraint in group.constraints:
            new_constraint = etree.SubElement(new_group, "constraint")
            new_constraint.set("type", constraint.type)
            new_constraint.set("relation", constraint.relation)
            new_constraint.text = f"{constraint.key}:{constraint.value}"

def delete_query(root, q_id):
    query = root.find(f".//*[@id='{str(q_id)}']")
    if query is not None:
        root.remove(query)

def save_file(tree, full_path_name):
    tree.write(full_path_name, encoding="utf-8", xml_declaration=False, pretty_print=True)