import bpy

def animate_emission_from_properties(curves, fps=24, duration=30, scale: float = 10.0, color=(0.0, 0.0, 1.0, 1)):
    # Calculate total frames for the animation
    total_frames = int(fps * duration)
    num_keys = 95  # t_0 to t_19
    frame_interval = total_frames // num_keys
    
    for curve in curves:
        # Create or assign a new emission material
        mat_name = f"EmissionMaterial_{curve.name}"
        if mat_name not in bpy.data.materials:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            emission_node = mat.node_tree.nodes.new('ShaderNodeEmission')
            output_node = mat.node_tree.nodes.get('Material Output')
            mat.node_tree.links.new(emission_node.outputs[0], output_node.inputs[0])
            
            # Set a constant emission color (e.g., soft pinkish)
            emission_node.inputs[0].default_value = color  # RGBA

            # Optional: Set a unique color for each curve based on a custom property
            # Uncomment if each curve has a unique color property (e.g., `color_r`, `color_g`, `color_b`)
            # emission_color = (
            #     curve.get("color_r", 1.0),
            #     curve.get("color_g", 1.0),
            #     curve.get("color_b", 1.0),
            #     1.0
            # )
            # emission_node.inputs[0].default_value = emission_color
            
        else:
            mat = bpy.data.materials[mat_name]
            emission_node = mat.node_tree.nodes.get('Emission')
        
        # Assign the material to the curve
        curve.data.materials.clear()
        curve.data.materials.append(mat)
        
        # Set keyframes for emission strength based on custom properties
        for t_idx in range(num_keys):
            frame = t_idx * frame_interval
            attr = curve.get(f"t_{t_idx}")
            if attr is None:
                attr = 1.0
            strength = (attr)**2 * scale
            if strength is not None:
                emission_node.inputs[1].default_value = strength
                emission_node.inputs[1].keyframe_insert(data_path="default_value", frame=frame)
                

def clear_matls(shapefile_name):
    for curve in bpy.data.collections.get(shapefile_name).objects:
        curve.data.materials.clear()
    
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)



# Example usage:
# Assuming the curves are in a collection called "your_curves_collection"
shapefile_name = "speed_smooth"
curves_collection = bpy.data.collections.get(shapefile_name)
curves = [obj for obj in curves_collection.objects if obj.type == 'CURVE']

#Run the function with curves, fps=30, duration=1 second, and color set to soft pinkish
#clear_matls(shapefile_name)
animate_emission_from_properties(curves, fps=24, duration=30, scale = 800, color=(0.8, 0.1, 0.0, 1))


        
