$(function() {
  $(".checkitem").click(function() {
    $(this).children("p").toggleClass("done");
  });

  $(".thumbnailexpander").click(function() {
    $(this).parent().next().children('.description').toggle()
  });
})

