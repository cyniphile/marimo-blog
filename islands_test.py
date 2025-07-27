from marimo import MarimoIslandGenerator

# Create the generator from file
generator = MarimoIslandGenerator.from_file(
    "./apps/Intro_to_Gaussian_Process_Regression.py", display_code=False
)

# Generate and print the HTML without building
# This will still work for basic rendering, though without running the cells
html = generator.render_html(include_init_island=False)
print(html)
# Save the HTML to a file
output_file = "output.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)
