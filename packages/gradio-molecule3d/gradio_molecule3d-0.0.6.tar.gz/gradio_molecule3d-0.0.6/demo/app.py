
import gradio as gr
from gradio_molecule3d import Molecule3D


example = Molecule3D().example_value()


reps =    [
    {
      "model": 0,
      "chain": "",
      "resname": "",
      "style": "stick",
      "color": "whiteCarbon",
      "residue_range": "",
      "around": 0,
      "byres": False,
      "visible": False
    }
  ]



def predict(x):
    print("predict function", x)
    print(x.name)
    return x

with gr.Blocks() as demo:
    gr.Markdown("# Molecule3D")
    inp = Molecule3D(label="Molecule3D", reps=reps)
    out = Molecule3D(label="Output", reps=reps)

    btn = gr.Button("Predict")
    gr.Markdown(""" 
    You can configure the default rendering of the molecule by adding a list of representations
    <pre>
        reps =    [
        {
          "model": 0,
          "style": "cartoon",
          "color": "whiteCarbon",
          "residue_range": "",
          "around": 0,
          "byres": False,
        },
        {
          "model": 0,
          "chain": "A",
          "resname": "HIS",
          "style": "stick",
          "color": "red"
        }
      ]
    </pre>
    """)
    btn.click(predict, inputs=inp, outputs=out)


if __name__ == "__main__":
    demo.launch()
