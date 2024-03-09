/*
	Dimension by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$wrapper = $('#wrapper'),
		$header = $('#header'),
		$footer = $('#footer'),
		$main = $('#main'),
		$main_articles = $main.children('article');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ '361px',   '480px'  ],
			xxsmall:  [ null,      '360px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Fix: Flexbox min-height bug on IE.
		if (browser.name == 'ie') {

			var flexboxFixTimeoutId;

			$window.on('resize.flexbox-fix', function() {

				clearTimeout(flexboxFixTimeoutId);

				flexboxFixTimeoutId = setTimeout(function() {

					if ($wrapper.prop('scrollHeight') > $window.height())
						$wrapper.css('height', 'auto');
					else
						$wrapper.css('height', '100vh');

				}, 250);

			}).triggerHandler('resize.flexbox-fix');

		}

	// Nav.
		var $nav = $header.children('nav'),
			$nav_li = $nav.find('li');

		// Add "middle" alignment classes if we're dealing with an even number of items.
			if ($nav_li.length % 2 == 0) {

				$nav.addClass('use-middle');
				$nav_li.eq( ($nav_li.length / 2) ).addClass('is-middle');

			}

	// Main.
		var	delay = 325,
			locked = false;

		// Methods.
			$main._show = function(id, initial) {

				var $article = $main_articles.filter('#' + id);
				console.log('article id:' + id);
				console.log('$article:' + $article);

				// No such article? Bail.
					if ($article.length == 0)
						return;

				// Handle lock.

					// Already locked? Speed through "show" steps w/o delays.
						if (locked || (typeof initial != 'undefined' && initial === true)) {

							// Mark as switching.
								$body.addClass('is-switching');

							// Mark as visible.
								$body.addClass('is-article-visible');

							// Deactivate all articles (just in case one's already active).
								$main_articles.removeClass('active');

							// Hide header, footer.
								$header.hide();
								$footer.hide();

							// Show main, article.
								$main.show();
								$article.show();

							// Activate article.
								$article.addClass('active');

							// Unlock.
								locked = false;

							// Unmark as switching.
								setTimeout(function() {
									$body.removeClass('is-switching');
								}, (initial ? 1000 : 0));

							return;

						}

					// Lock.
						locked = true;

				// Article already visible? Just swap articles.
					if ($body.hasClass('is-article-visible')) {

						// Deactivate current article.
							var $currentArticle = $main_articles.filter('.active');

							$currentArticle.removeClass('active');

						// Show article.
							setTimeout(function() {

								// Hide current article.
									$currentArticle.hide();

								// Show article.
									$article.show();

								// Activate article.
									setTimeout(function() {

										$article.addClass('active');

										// Window stuff.
											$window
												.scrollTop(0)
												.triggerHandler('resize.flexbox-fix');

										// Unlock.
											setTimeout(function() {
												locked = false;
											}, delay);

									}, 25);

							}, delay);

					}

				// Otherwise, handle as normal.
					else {

						// Mark as visible.
							$body
								.addClass('is-article-visible');

						// Show article.
							setTimeout(function() {

								// Hide header, footer.
									$header.hide();
									$footer.hide();

								// Show main, article.
									$main.show();
									$article.show();

								// Activate article.
									setTimeout(function() {

										$article.addClass('active');

										// Window stuff.
											$window
												.scrollTop(0)
												.triggerHandler('resize.flexbox-fix');

										// Unlock.
											setTimeout(function() {
												locked = false;
											}, delay);

									}, 25);

							}, delay);

					}

			};

			$main._hide = function(addState) {

				var $article = $main_articles.filter('.active');

				// Article not visible? Bail.
					if (!$body.hasClass('is-article-visible'))
						return;

				// Add state?
					if (typeof addState != 'undefined'
					&&	addState === true)
						history.pushState(null, null, '#');

				// Handle lock.

					// Already locked? Speed through "hide" steps w/o delays.
						if (locked) {

							// Mark as switching.
								$body.addClass('is-switching');

							// Deactivate article.
								$article.removeClass('active');

							// Hide article, main.
								$article.hide();
								$main.hide();

							// Show footer, header.
								$footer.show();
								$header.show();

							// Unmark as visible.
								$body.removeClass('is-article-visible');

							// Unlock.
								locked = false;

							// Unmark as switching.
								$body.removeClass('is-switching');

							// Window stuff.
								$window
									.scrollTop(0)
									.triggerHandler('resize.flexbox-fix');

							return;

						}

					// Lock.
						locked = true;

				// Deactivate article.
					$article.removeClass('active');

				// Hide article.
					setTimeout(function() {

						// Hide article, main.
							$article.hide();
							$main.hide();

						// Show footer, header.
							$footer.show();
							$header.show();

						// Unmark as visible.
							setTimeout(function() {

								$body.removeClass('is-article-visible');

								// Window stuff.
									$window
										.scrollTop(0)
										.triggerHandler('resize.flexbox-fix');

								// Unlock.
									setTimeout(function() {
										locked = false;
									}, delay);

							}, 25);

					}, delay);


			};

		// Articles.
			$main_articles.each(function() {

				var $this = $(this);

				// Close.
					$('<div class="close">Close</div>')
						.appendTo($this)
						.on('click', function() {
							location.hash = '';
						});

				// Prevent clicks from inside article from bubbling.
					$this.on('click', function(event) {
						event.stopPropagation();
					});

			});

		// Events.
			$body.on('click', function(event) {

				// Article visible? Hide.
					if ($body.hasClass('is-article-visible'))
						$main._hide(true);

			});

			$window.on('keyup', function(event) {

				switch (event.keyCode) {

					case 27:

						// Article visible? Hide.
							if ($body.hasClass('is-article-visible'))
								$main._hide(true);

						break;

					default:
						break;

				}

			});

			$window.on('hashchange', function(event) {

				// Empty hash?
					if (location.hash == ''
					||	location.hash == '#') {

						// Prevent default.
							event.preventDefault();
							event.stopPropagation();

						// Hide.
							$main._hide();

					}

				// Otherwise, check for a matching article.
					else if ($main_articles.filter(location.hash).length > 0) {

						// Prevent default.
							event.preventDefault();
							event.stopPropagation();

						// Show article.
							$main._show(location.hash.substr(1));

					}

			});

		// Scroll restoration.
		// This prevents the page from scrolling back to the top on a hashchange.
			if ('scrollRestoration' in history)
				history.scrollRestoration = 'manual';
			else {

				var	oldScrollPos = 0,
					scrollPos = 0,
					$htmlbody = $('html,body');

				$window
					.on('scroll', function() {

						oldScrollPos = scrollPos;
						scrollPos = $htmlbody.scrollTop();

					})
					.on('hashchange', function() {
						$window.scrollTop(oldScrollPos);
					});

			}

		// Initialize.

			// Hide main, articles.
				$main.hide();
				$main_articles.hide();

			// Initial article.
				if (location.hash != ''
				&&	location.hash != '#')
					$window.on('load', function() {
						$main._show(location.hash.substr(1), true);
					});

		//Cloud9Shoe scripts
		// var slider = document.getElementById("motorIntensity");
		// var output = document.getElementById("motorIntensityValue");
		// output.innerHTML = slider.value; // Display the default slider value

		// // Update the current slider value (each time you drag the slider handle)
		// slider.oninput = function() {
		// 	output.innerHTML = this.value;
		// 	var selected = this.value;
		// 	if (selected == 1){
		// 		stopsign.src = "assets/icons/start.png";
		// 		crawl.src = "assets/icons/turtle_nocolor.png";
		// 		walk.src = "assets/icons/walking_nocolor.png";
		// 		run.src = "assets/icons/running_nocolor.png";
		// 		fly.src = "assets/icons/jet_nocolor.png"
		// 	}
		// 	else if (selected == 2){
		// 		stopsign.src = "assets/icons/stop.png";
		// 		crawl.src = "assets/icons/turtle_color.png";
		// 		walk.src = "assets/icons/walking_nocolor.png";
		// 		run.src = "assets/icons/running_nocolor.png";
		// 		fly.src = "assets/icons/jet_nocolor.png"
		// 	} else if (selected == 3){
		// 		stopsign.src = "assets/icons/stop.png";
		// 		crawl.src = "assets/icons/turtle_nocolor.png";
		// 		walk.src = "assets/icons/walking_color.png";
		// 		run.src = "assets/icons/running_nocolor.png";
		// 		fly.src = "assets/icons/jet_nocolor.png"
		// 	}else if (selected == 4){
		// 		stopsign.src = "assets/icons/stop.png";
		// 		crawl.src = "assets/icons/turtle_nocolor.png";
		// 		walk.src = "assets/icons/walking_nocolor.png";
		// 		run.src = "assets/icons/running_color.png";
		// 		fly.src = "assets/icons/jet_nocolor.png"
		// 	}else if (selected == 5){
		// 		stopsign.src = "assets/icons/stop.png";
		// 		crawl.src = "assets/icons/turtle_nocolor.png";
		// 		walk.src = "assets/icons/walking_nocolor.png";
		// 		run.src = "assets/icons/running_nocolor.png";
		// 		fly.src = "assets/icons/jet_color.png"
		// 	}
		// 	setMotorIntensity(selected)

		// }

/* 		$.post({
			url: "/api/endpoint",
			contentType: "application/json",
			data: JSON.stringify({ key: value }),
			success: function(response) {
				// Handle the response here
			},
			error: function(xhr, status, error) {
				// Handle errors
			}
		}); */

		// $('.slider a').live('click', function(e) {
		// 	alert('Button clicked! ID=' + $(this).attr('id'));

		// });

		// $('.slide-control').click(function(evt) {
		// 	evt.preventDefault();
		// 	alert('Button clicked! ID=' + $(this).attr('id'));
		// 	var divId = 'summary' + $(this).attr('id');
	
		// 	//document.getElementById(divId).className = '';
	
		// });

		// $('#slider1').on('click', function() {
		// 	alert('Button clicked! ID=' + $(this).attr('id'));

		// });
		

		// $(".solTitle a").live('click',function(e){
        //     var contentId = "summary_" + $(this).attr('id');
        //     $(".summary").hide();
        //     $("#" + contentId).show();
        // });

		// var $slider1 = $('slider1');
		// alert($slider1);
		// $slider1.on('click', setMotorIntensity(0))
		// slider1.onclick =setMotorIntensity(0)

		

		$('#btnDiagnose').on('click', function() {
			alert('Button clicked!');
			$.get({
				url: "/accel" ,
				contentType: "application/json",
				success: function(response) {
					// Handle the response here
					console.log(response);
				},
				error: function(xhr, status, error) {
					// Handle errors
					console.log(error);
				}
			});
		});

})(jQuery);

function setMotorIntensity(level) {
	let postData = {
	"action": "motor",
	"level": level
	};
	console.log('postData'+ postData);
	$.post({
		url: "/motor/control" ,
		contentType: "application/json",
		data: JSON.stringify(postData),
		success: function(response) {
			// Handle the response here
			console.log(response);
		},
		error: function(xhr, status, error) {
			// Handle errors
			console.log(error);
		}
	});		
}

/* function getAccelData() {
	alert('Button clicked!');
	$.get({
		url: "/accel" ,
		contentType: "application/json",
		success: function(response) {
			// Handle the response here
			console.log(response);
		},
		error: function(xhr, status, error) {
			// Handle errors
			console.log(error);
		}
	});
} */
