from flask import Flask
from flask import render_template
import FoamAna as fa
from bokeh.embed import components
from bokeh.widgets import HBox, Paragraph, Slider, VBox
from bokeh.utils import encode_utf8


from bokeh.resources import Resources
from bokeh.templates import RESOURCES


app = Flask(__name__)

@app.route('/')
def root():
    resources = Resources("inline")
    scatter = scatter_example()

    scatter_el = VBox(children=[HBox(children=[scatter])])

    plot_script, plot_div = components(scatter_el, resources)

    plot_resources = RESOURCES.render(
        js_raw = resources.js_raw,
        css_raw = resources.css_raw,
        js_files = resources.js_files,
        css_files = resources.css_files,
    )

    html = render_template("test.html",
         plot_resources = plot_resources,
         plot_script = plot_script,
         plot_div = plot_div 
        )
    return encode_utf8(html) 


def scatter_example():
    from bokeh.plotting import output_server
    from bokeh.plotting import show
    props = fa.PlotProperties()
    s1 = fa.read_sets(
            folder='/home/go/documents/code/FoamAna/examples/buoyantCavity/',
            name='foo',
            plot_properties=props
         )
    return (s1
            .by(name='Loc', index=lambda x: x)
            .scatter(x='Pos',y='T', x_label="Position [m]", y_label="Temp [K]"))

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
    
