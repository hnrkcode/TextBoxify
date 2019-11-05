Example
=======

This example is based of the code in ``examples/example.py``

This is how you could initialize and customize a dialog box with ``TextBoxFrame``,
which creates a dialog box with a border and optional features like animated portrait and idling symbol::

    dialog_box = textboxify.TextBoxFrame(
        text=dialog_text,
        text_width=320,
        lines=2,
        pos=(80, 180),
        padding=(150, 100),
        font_color=(92, 53, 102),
        font_size=26,
        bg_color=(173, 127, 168))


Add these two lines to create a symbol indicating that the box is idle and a picture representing the character talking::

    dialog_box.set_indicator()
    dialog_box.set_portrait()


To implement the text box you could add it to a sprite group, like ``pygame.sprite.LayeredDirty`` because the text boxes are subclasses of ``pygame.sprite.DirtySprite``.

To activate the textbox you then add the text box object to the sprite group::

    if not dialog_group:
        dialog_group.add(dialog_box)

You can check if all words has pin printed, if there are still words to print,
you can continue printing the remaining words by reseting the box so the words
in the box are erased like this::

    if dialog_box.words:
        dialog_box.reset()

If there isn't any words left to print you can close the box with::

    else:
        dialog_box.kill()

That will deactivate the box and remove it from the sprite group.
If you want to reuse the text box, you should first call ``reset(hard=True)`` and if you also want to set a new message call ``set_text()``::

    dialog_box.reset(hard=True)
    dialog_box.set_text("Happy coding!")


For a working example of how to implement `textboxify` see the example module.
