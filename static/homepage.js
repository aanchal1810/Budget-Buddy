$(document).ready(function(){$(".flex-slide").each(function () {
    $(this).hover(
      function () {
        $(this).find(".flex-title").css({
          transform: "rotate(0deg)",
          top: "5%"
        });
        $(this).find(".flex-about").css({
          opacity: "1"
        });
      },
      function () {
        $(this).find(".flex-title").css({
          transform: "rotate(90deg)",
          top: "15%"
        });
        $(this).find(".flex-about").css({
          opacity: "0"
        });
      }
    );
  });
});

$(document).ready(function() {
  $("#menuicon").click(function() {
      $(this).css({
          'transform': $(this).css('transform') === 'none' ? 'rotate(90deg)' : 'none',
          'transition': 'transform 0.5s ease-in-out'

      });
      $("#hiddenmenu").toggle(300); 
  });
});

  