import bpy


def emission_node_builder(shapefile_name: str,  scale: float = 1.0):

    network_connection = bpy.data.collection.get(shapefile_name)

    base_material = bpy.data.materials.new(name="EmissiveMaterial")
    base_material.use_nodes = True
    nodes = base_material.node_tree.nodes
    nodes.clear()

    emission_node = nodes.new(type="ShaderNodeEmission")
    emission_node.inputs["color"].default_value = (1.0, 0.0, 0.0, 1.0)

    output_node = nodes.new("ShaderNodeOutputMaterial")
    output_links = base_material.node_tree.links
    output_links.new(emission_node.outputs["Emision"], output_node.inputs["Surface"])

    for link in network_collection.objects:
        if link.type == "CURVE":
            emissivity: float = link["FRC"]

        curve_material = base_material.copy()
        curve_material.node_tree.nodes['Emission'].inputs['Strength'].default_value = emissivity * scale

        if link.data.materials:
            link.data.materials[0] = curve_material
        else:
            link.data.materials.append(curve_material)


def main():

    emission_node_builder()


if __name__ == "__main__":
    main()
