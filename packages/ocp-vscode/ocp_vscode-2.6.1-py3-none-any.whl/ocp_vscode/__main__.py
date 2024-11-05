import click
import socket
import yaml
from pathlib import Path
from ocp_vscode.standalone import Viewer, DEFAULTS, CONFIG_FILE
from ocp_vscode.state import resolve_path


def represent_list(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)


yaml.add_representer(list, represent_list)


@click.command()
@click.option(
    "--create_configfile",
    is_flag=True,
    help="Create the configlie .ocpvscode_standalone in the home directory",
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="The host to start OCP CAD with",
)
@click.option(
    "--port",
    default=3939,
    help="The port to start OCP CAD with",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Show debugging information",
)
@click.option(
    "--timeit",
    is_flag=True,
    help="Show timing information",
)
@click.option(
    "--tree_width",
    help="OCP CAD Viewer navigation tree width (default: 240)",
)
@click.option(
    "--no_glass",
    is_flag=True,
    help="Do not use glass mode with transparent navigation tree",
)
@click.option(
    "--theme",
    default="light",
    help="Use theme 'light' or 'dark' (default: 'light')",
)
@click.option(
    "--no_tools",
    is_flag=True,
    help="Do not show toolbar",
)
@click.option(
    "--tree_width", default=240, help="Width of the CAD navigation tree (default: 240)"
)
@click.option(
    "--control",
    default="trackball",
    help="Use control mode 'orbit'or 'trackball'",
)
@click.option(
    "--up",
    default="Z",
    help="Provides up direction, 'Z', 'Y' or 'L' (legacy) (default: Z)",
)
@click.option(
    "--rotate_speed",
    default=1,
    help="Rotation speed (default: 1)",
)
@click.option(
    "--zoom_speed",
    default=1,
    help="Zoom speed (default: 1)",
)
@click.option(
    "--pan_speed",
    default=1,
    help="Pan speed (default: 1)",
)
@click.option(
    "--axes",
    is_flag=True,
    help="Show axes",
)
@click.option(
    "--axes0",
    is_flag=True,
    help="Show axes at the origin (0, 0, 0)",
)
@click.option(
    "--black_edges",
    is_flag=True,
    help="Show edges in black",
)
@click.option(
    "--grid_xy",
    is_flag=True,
    help="Show grid on XY plane",
)
@click.option(
    "--grid_yz",
    is_flag=True,
    help="Show grid on YZ plane",
)
@click.option(
    "--grid_xz",
    is_flag=True,
    help="Show grid on XZ plane",
)
@click.option(
    "--center_grid",
    is_flag=True,
    help="Show grid planes crossing at center of object or global origin(default: False)",
)
@click.option(
    "--collapse",
    default=1,
    help="leaves: collapse all leaf nodes, all: collapse all nodes, none: expand all nodes, root: expand root only (default: leaves)",
)
@click.option(
    "--perspective",
    is_flag=True,
    help="Use perspective camera",
)
@click.option(
    "--ticks",
    default=10,
    help="Default number of ticks (default: 10)",
)
@click.option(
    "--transparent",
    is_flag=True,
    help="Show objects transparent",
)
@click.option(
    "--default_opacity",
    default=0.5,
    help="Default opacity for transparent objects (default: 0.5)",
)
@click.option(
    "--explode",
    is_flag=True,
    help="Turn explode mode on",
)
@click.option(
    "--angular_tolerance",
    default=0.2,
    help="Angular tolerance for tessellation algorithm (default: 0.2)",
)
@click.option(
    "--deviation",
    default=0.1,
    help="Deviation of for tessellation algorithm (default: 0.1)",
)
@click.option(
    "--default_color",
    default="#e8b024",
    help="Default shape color, CSS3 color names are allowed (default: #e8b024)",
)
@click.option(
    "--default_edgecolor",
    default="#707070",
    help="Default color of the edges of shapes, CSS3 color names are allowed (default: #707070)",
)
@click.option(
    "--default_thickedgecolor",
    default="MediumOrchid",
    help="Default color of lines, CSS3 color names are allowed (default: MediumOrchid)",
)
@click.option(
    "--default_facecolor",
    default="Violet",
    help="Default color of faces, CSS3 color names are allowed (default: Violet)",
)
@click.option(
    "--default_vertexcolor",
    default="MediumOrchid",
    help="Default color of vertices, CSS3 color names are allowed (default: MediumOrchid)",
)
@click.option(
    "--ambient_intensity",
    default=1,
    help="Intensity of ambient light (default: 1.00)",
)
@click.option(
    "--direct_intensity",
    default=1.1,
    help="Intensity of direct light (default: 1.10)",
)
@click.option(
    "--metalness",
    default=0.3,
    help="Metalness property of material (default: 0.30)",
)
@click.option(
    "--roughness",
    default=0.65,
    help="Roughness property of material (default: 0.65)",
)
def main(*args, **kwargs):
    if kwargs.get("create_configfile"):

        config_file = Path(resolve_path(CONFIG_FILE))
        with open(config_file, "w") as f:
            f.write(yaml.dump(DEFAULTS))
        print(f"Created config file {config_file}")

    else:
        viewer = Viewer(kwargs)

        port = kwargs["port"]
        host = kwargs["host"]

        if host == "0.0.0.0":
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)

        print(f"\nThe viewer is running at http://{host}:{port}/viewer\n")

        viewer.start()


if __name__ == "__main__":
    main()
