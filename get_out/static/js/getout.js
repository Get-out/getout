$(function() {
  $(".checkitem").click(function() {
    $(this).toggleClass("done");
  });

  $(".thumbnailexpander").click(function(event) {
    $(this).parent().next().children('.description').toggle()
    event.stopPropagation()
  });

})

