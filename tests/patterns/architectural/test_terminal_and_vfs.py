from playwright.sync_api import Page, expect


def test_virtual_terminal_output(page: Page, live_server: str):
    page.goto(f"{live_server}/examples/loading/virtual_terminal.html")

    output = page.locator("#term-output")
    expect(output).to_contain_text("Python Virtual Terminal Ready.", timeout=30000)

    # Test typing an expression
    cmd_input = page.locator("#term-input")
    cmd_input.fill("10 + 10")
    cmd_input.press("Enter")

    expect(output).to_contain_text(">>> 10 + 10")
    expect(output).to_contain_text("20")


def test_vfs_explorer_rendering(page: Page, live_server: str):
    page.goto(f"{live_server}/examples/loading/vfs_explorer.html")

    # 1. Wait for the loading message to disappear, indicating Python is ready
    root_node = page.locator("#fs-root")
    expect(root_node).not_to_contain_text("Loading VFS...", timeout=60000)

    # 2. Verify tree content
    # For /home, the basename is 'home'
    expect(root_node).to_contain_text("📁 home")
    expect(root_node).to_contain_text("📄 hello.py")
    expect(root_node).to_contain_text("📁 data")
