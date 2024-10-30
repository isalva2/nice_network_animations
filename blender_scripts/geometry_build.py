import bpy
import bmesh
from mathutils import Vector, Matrix


def network_global_rescale(shapefile_name: str, scale: float = 0.01):
    # get collectinon containing all links in network
    network_collection = bpy.data.collections.get(shapefile_name)

    for link in network_collection.objects:
        if (link.type == "MESH"):

            original_location = link.location.copy()

            # Scale the object down by 90%
            link.scale = (scale, scale, scale)

            # Calculate the new location
            new_location = (
                original_location.x * scale,  # Adjusted for scaling
                original_location.y * scale,
                original_location.z * scale
            )

            # Update the object's location
            link.location = new_location


def convert_to_curve(link):

    bpy.context.view_layer.objects.active = link
    link.select_set(True)

    # Convert the mesh to a curve
    bpy.ops.object.convert(target='CURVE')


bevel_map = {
    "1": 70,
    "2": 60,
    "2": 50, 
    "3": 40,
    "4": 30,
    "5": 20,
}


def bevel_curve(link, scale):
    link_depth = bevel_map[link["FRC"]] * scale
    link.data.bevel_depth = link_depth
    link.data.bevel_resolution = 2
    link.data.fill_mode = "FULL"
#    link.data.dimensions = "2D"
#    link.data.resolution_u = 6
#    link.data.resolution_v = 6


def build_network_geometry(shapefile_name: str, scale: float = 0.01):
    # get collectinon containing all links in network
    network_collection = bpy.data.collections.get(shapefile_name)

    # convert mesh to curve
    for link in network_collection.objects:
        if (link.type == "MESH"):
            convert_to_curve(link)

    # add bevel properties to curve
    for link in network_collection.objects:
        if (link.type == "CURVE"):
            bevel_curve(link, scale = 0.2)


def print_network_fields(shapefile_name: str):
    field_set = set()
    for link in bpy.data.collections.get(shapefile_name).objects:
        if link.type == "MESH":
            for K in link.keys():
                if K not in '_RNA_UI':
                    field_set.add(K)
    print(f"Fields imported: {field_set}")


def main():
    network_global_rescale("speed_smooth")
    build_network_geometry("speed_smooth")


if __name__ == "__main__":
    main()
