import bpy
import math


def strength_scaler(x: float, mode: str):
    if mode == "linear":
        return x
    if mode == "smooth":
        return 3 * x**2 - 2 * x**3
    if mode == "exp":
        k = 10
        return (math.exp(k*10) - 1) / (math.exp(k) - 1)
    else:
        return x


def emission_node_builder(network_collection, step: str, scale: float = 10.0):
    # create base
    base_material = bpy.data.materials.new(name=f"Material_{step}")
    base_material.use_nodes = True
    nodes = base_material.node_tree.nodes
    nodes.clear()

    emission_node = nodes.new(type="ShaderNodeEmission")
    emission_node.inputs["Color"].default_value = (0.0, 0.0, 1.0, 1)

    output_node = nodes.new("ShaderNodeOutputMaterial")
    output_links = base_material.node_tree.links
    output_links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])

    for link in network_collection.objects:
        if link.type == "CURVE":
            emissivity: float = float(link[step])

        curve_material = base_material.copy()
        curve_material.node_tree.nodes['Emission'] \
            .inputs['Strength'].default_value = 10 + strength_scaler(emissivity, "smooth") * scale

        # append multiple materials to curve
        if link.data.materials:
            link.data.materials.append(curve_material)
        else:
            link.data.materials.append(curve_material)
            

def remove_all_materials(network_collection):
    if network_collection:
        for link in network_collection.objects:
            if link.data.materials:
                link.data.materials.clear()


def main(shapefile_name, scale, n_frames):
    network_collection = bpy.data.collections.get(shapefile_name)
    emission_node_builder(network_collection, "t_0", scale)
            

def generate_hour_index():
    indices = []
    current_index = 1
    step =   2

    while current_index <= 96:
        indices.append(current_index)
        current_index += step

    return indices


def hour_cycle():
    network_collection = bpy.data.collections.get("rectangle")
    
    frame_indices = generate_hour_index()
    
    for frame in frame_indices:
        emission_node_builder(network_collection, f"t_{frame}", 700)
    

if __name__ == "__main__":
    hour_cycle()
