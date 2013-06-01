$(function() {
  $(".thumbnailexpander").click(function() {
    $(this).parent().next().children('.description').toggle()
  });

  $(".checkitem").click(function() {
    $(this).children("p").toggleClass("done");
  });

})

