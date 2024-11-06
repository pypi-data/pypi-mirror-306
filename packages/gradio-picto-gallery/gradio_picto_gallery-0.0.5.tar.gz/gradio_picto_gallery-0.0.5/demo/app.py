import gradio as gr
from gradio_picto_gallery import PictoGallery

example = PictoGallery().example_value()
payload = PictoGallery().example_payload()

with gr.Blocks() as demo:
    with gr.Row():
        gallery = PictoGallery(
            value=example,
            height=1000,
            min_width=500,
            object_fit="scale_down",
            interactive=False,
            hide_close_button=True,
        )  #

    def on_toggle_favorite(value, evt: gr.EventData):
        favorite = evt._data["favorite"]
        if favorite:
            # add here logic to save the image to favorites
            print(f"Add {evt._data['image']['orig_name']} to favorites")
        else:
            # add here logic to remove the image from favorites
            print(f"Remove {evt._data['image']['orig_name']} from favorites")

    def on_like(evt: gr.EventData):
        print(f"Like {evt._data['image']['orig_name']}")

    def on_dislike(evt: gr.EventData):
        print(f"Dislike {evt._data['image']['orig_name']}")

    gallery.toggle_favorite(on_toggle_favorite, gallery, None)
    gallery.like(on_like, None, None)
    gallery.dislike(on_dislike, None, None)


if __name__ == "__main__":
    demo.launch()
