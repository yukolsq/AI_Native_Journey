document.querySelectorAll('.format-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const command = btn.getAttribute('data-command');
    document.execCommand(command, false, null);
  });
});

// Emoji picker logic
const picker = new EmojiButton();

const trigger = document.querySelector('.emoji-btn');
const body = document.querySelector('.body');

picker.on('emoji', emoji => {
  const selection = window.getSelection();
  if (!selection.rangeCount) return;
  selection.getRangeAt(0).insertNode(document.createTextNode(emoji));
});

trigger.addEventListener('click', () => {
  picker.togglePicker(trigger);
});


  