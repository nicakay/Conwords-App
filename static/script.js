$(document).ready(function() {

    // Script that enables editing a selected field on the 'dictionary' page

    $(".edit").on("dblclick", "input, select", function(){

        $(this)
        .prop("readonly", false)
        .removeClass("toedit")
        .siblings("span").hide();
    
        $(saveRecord)
        .prop("disabled", false);
    });
    
    $(".edit").on("blur", "input, select", function(){
        $(this)
        .prop("readonly", true)
        .addClass("toedit")
        .siblings("span").text($(this).val()).show();
    });
    
    $("#editRecord").on("click", "td", function(){
        $(".edit").children().focus();
    });

    // The switch button that toggles between the word and the meaning view in the dictionary

    $("#wordsMeaningsToggle").on("change", function() {
        $("#left-menu-words").toggle();
        $("#left-menu-meanings").toggle();
    });

});

// Highlights selected word parts on the 'Settings' page

$(function() {
    $(".delete-word-part-btn").hover(function() {
        $(this).parent().parent().css("background-color", "#b9effc")
    }, function() {
        $(this).parent().parent().css("background-color", "#fff")
    });
});


// Function to copy a word to the clipboard
async function copyWord() {

  event.preventDefault();
  
  // Copies the inside text of the second parent, but LOL it copies also extra spaces and the Copy word from thr button...
  let textToCopy = $(event.target).parent().parent().text();

  // Temporary workaround - Remove 'Copy' then remove all the spaces
  textToCopy = textToCopy.replace('Copy', '');
  textToCopy = textToCopy.replace(/\s/g, '');

  // Navigator clipboard api needs a secure context (https)
  if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(textToCopy);
  } else {
      // Use the 'out of viewport hidden text area' trick
      const textArea = document.createElement("textarea");
      textArea.value = textToCopy;
          
      // Move textarea out of the viewport so it's not visible
      textArea.style.position = "absolute";
      textArea.style.left = "-999999px";
          
      document.body.prepend(textArea);
      textArea.select();

      try {
          document.execCommand('copy');
      } catch (error) {
          console.error(error);
      } finally {
          textArea.remove();
      }
  };
}
