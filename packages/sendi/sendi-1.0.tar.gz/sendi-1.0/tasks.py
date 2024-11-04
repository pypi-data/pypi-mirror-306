from invoke import Context, task


@task
def init(context: Context) -> None:
    """
    Initialize the context
    """
    context.run("rye self update", warn=True)
    context.run("rye pin 3.11", warn=True)
    context.run("rye tools install -f invoke", warn=True)
    context.run("rye tools install -f gitlabci-local", warn=True)
    context.run("rye sync", warn=True)
    context.run("rye install pre-commit", warn=True)
    context.run("rye run pre-commit install", warn=True)
    context.run("rye run uv pip compile pyproject.toml -o requirements.txt", warn=True)


@task
def check(context: Context) -> None:
    context.run("rye run pre-commit run --all-files", pty=True)


@task
def build(context: Context) -> None:
    """
    Build
    """
    context.run("rye show", warn=True)
    context.run("rye build --clean", warn=True)


@task
def init_deb(context: Context) -> None:
    context.run("rye tools install -f wheel2deb")
    context.run("sudo apt update")
    context.run("sudo apt install apt-file dpkg-dev fakeroot build-essential devscripts debhelper")
    context.run("sudo apt-file update")


@task
def build_deb(context: Context) -> None:
    """
    Build deb from wheel
    """
    context.run("pip wheel -w dist omemo>=1.1.0 annotated-types>=0.5.0 slixmpp-omemo>=1.1.1")
    context.run("wheel2deb default --search-path dist/ --output-dir deb", warn=True)


@task
def container_build(
    context: Context,
    label: str = "sendi",
    repository: str = "localhost",
    platform: str = "linux/amd64",
    version: str = "1.0.0",
) -> None:
    command_line = "buildah bud"
    command_line += (
        f' --tag "{repository}/{label}:{version}" --platform {platform} --build-arg TAG="build_{version}"'
    )
    command_line += " ."
    context.run(command_line)
