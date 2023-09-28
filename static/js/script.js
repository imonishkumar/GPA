// ==========================================================================
//	Multi-level accordion nav
// ==========================================================================
$('.acnav__label').click(function () {
	var label = $(this);
	var parent = label.parent('.has-children');
	var list = label.siblings('.acnav__list');

	if ( parent.hasClass('is-open') ) {
		list.slideUp('slow');
		parent.removeClass('is-open');
	}
	else {
		list.slideDown('slow');
		parent.addClass('is-open');
	}
});
// ==========================================================================
