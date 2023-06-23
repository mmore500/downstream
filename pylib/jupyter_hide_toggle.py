import random

from IPython.display import HTML, Javascript

def jupyter_hide_toggle(hide: bool = False):
    if hide:
        return _jupyter_hide_toggle_hide()
    else:
        return _jupyter_hide_toggle_show()


# adapted from https://stackoverflow.com/a/52664156
def _jupyter_hide_toggle_hide():
    js_code = """
    function createToggleButton(cell) {
        var toggle_button = $('<button>').text('Toggle Input').click(function () {
            var input_area = cell.find('.input');
            input_area.toggle();
        });

        // Append button to the cell's toolbar
        cell.find('.input').before(toggle_button);

        // Hide input area by default
        cell.find('.input').hide();
    }

    var output_area = this;

    // Find the parent cell element
    var cell_element = output_area.element.parents('.cell');

    // Create toggle button for this cell
    createToggleButton(cell_element);
    """

    return Javascript(js_code)


def _jupyter_hide_toggle_show():
    this_cell = """$('div.cell.code_cell.rendered.selected')"""

    toggle_text = "Toggle show/hide"  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle

    js_f_name = "code_toggle_{}".format(str(random.randint(1, 2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        toggle_text=toggle_text,
    )

    return HTML(html)
