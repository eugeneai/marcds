// Jquery with no conflict
jQuery(document).ready(function($) {   
	
	
	//##########################################
	// FIX FOOTER AT BOTTOM
	//##########################################	
	function fixFooterBottom(){
		var h = $('#scroll-holder').height()*2;
		$('#footer-container-fixed').css({
			marginTop: function(index, value){ return h }
		});
	}
	
	
    //##########################################
	// Tweet feed
	//##########################################
	
	$("#tweets").tweet({
        query: "from:ansimuz http",
        count: 3,
        loading_text: "loading tweets..."
    });
    
    //##########################################
	// Tool tips
	//##########################################
	
    $('.poshytip').poshytip({
    	className: 'tip-twitter',
		showTimeout: 1,
		alignTo: 'target',
		alignX: 'center',
		offsetY: 5,
		allowTipHover: false
    });
    
    $('.form-poshytip').poshytip({
		className: 'tip-yellowsimple',
		showOn: 'focus',
		alignTo: 'target',
		alignX: 'right',
		alignY: 'center',
		offsetX: 5
	});
	
    //##########################################
	// Rollover
	//##########################################

	$("#sidebar li a").hover(function() { 
		// on rollover	
		$(this).stop().animate({ 
			marginLeft: "8" 
		}, "fast");
	} , function() { 
		// on out
		$(this).stop().animate({
			marginLeft: "0" 
		}, "fast");
	});
    
	//##########################################
	// Bg stretcher
	//##########################################

	var theWindow        = $(window),
	    $bg              = $("#bg"),
	    aspectRatio      = $bg.width() / $bg.height()
	    originalBg       = $bg.attr('src');
	                                        
	function resizeBg() {
		$bg              = $("#bg");
		aspectRatio      = $bg.width() / $bg.height();
		
	    if ( (theWindow.width() / theWindow.height()) < aspectRatio ) {
	        $bg
	            .removeClass()
	            .addClass('bgheight');
	    } else {
	        $bg
	            .removeClass()
	            .addClass('bgwidth');
	    }	    
	}
		                                        
	//##########################################
	// Scrolling bar
	//##########################################
	
	function starScrolling(){
		$("div#makeMeScrollable").smoothDivScroll({ 
			autoScroll: "onstart" , 
			autoScrollDirection: "backandforth", 
			autoScrollStep: 1, 
			autoScrollInterval: 15,	
			startAtElementId: "startAtMe",
			visibleHotSpots: "always"
		});
	};

	// centers the scroll on resize
	
	function centerScroll(){
		var h = $(window).height()/2 - $('#scroll-holder').height()/2;
		$('#scroll-holder').css({
			top: function(index, value){ return h }
		});
	}
	
	
	
	// Click image, Open image on background
	
	$("div#makeMeScrollable a").click(function(){
		// set description
		img_title = $(this).attr('title');
		img_desc = $(this).children('img').attr('alt');
		setImageDescription(img_title, img_desc);
			
		// Display image buttons
		$("#image-buttons").show();
		$('#nav').hide();
		
		$('#bg').hide('');
		
		// put loader image
		$('#no-bg-click').addClass('loading-img');
	
		var sr = $(this).attr('href');
		$("div#makeMeScrollable").hide();
		// load image on Bg and call resizeBg
		imgLoader(sr);
		return false;
	});
	
	// Close button
	
	$('#image-buttons #close-image').click(function(){
		// show
		$("div#makeMeScrollable").fadeIn();
		$("div#gallery-holder").fadeIn();
		
		imgLoader(originalBg);
		resizeBg();
		centerScroll();
		fixFooterBottom();
		
		// hide
		$('#image-buttons').hide();
		$('#image-description').hide();
		$('#nav').show();
		
		
	});
	
	// Open description
	
	$('#image-buttons #info-button').click(function(){
		$('#image-description').fadeToggle();
	})
	
	// function image loader
	
	function imgLoader(sr){
		$('#bg').load(function() {
		  resizeBg();
		  $('#no-bg-click').removeClass('loading-img');
		  
		  $('#bg').hide().fadeIn();
		}).attr('src', sr);
	}
	
	//##########################################
	// Footer toggle
	//##########################################
	
	var footerContainer = jQuery('#footer-container');
	var footerTrigger = jQuery('#footer-open a');
	
	var footerContainerHeight = footerContainer.height() + 3;

	footerContainer.css({
		marginBottom : -footerContainerHeight,
		display : 'block'
	});
	
	footerTrigger.toggle( function() {
	
		footerContainerHeight = footerContainer.height() + 3;
		
		footerContainer.animate({
			marginBottom : 0
		}, 700, 'easeOutExpo');
		footerTrigger.addClass('footer-close');
	}, function() {
		footerContainer.animate({
			marginBottom : -footerContainerHeight
		}, 700, 'easeOutExpo');
		footerTrigger.removeClass('footer-close');
	});

		
	//##########################################
	// Resize event
	//##########################################
	
	theWindow.resize(function() {
	    resizeBg();
	    centerScroll();
	    fixFooterBottom();
	}).trigger("resize");
	
	//##########################################
	// Pretty photo
	//##########################################
	
	$("a[rel^='prettyPhoto']").prettyPhoto();
	
	
	//##########################################
	// Nav menu
	//##########################################
	
	$("ul.sf-menu").superfish({ 
        animation: {height:'show'},   // slide-down effect without fade-in 
        delay:     800 ,              // 1.2 second delay on mouseout 
        autoArrows:  false,
        speed:         'normal'
    });


	//##########################################
	// QUICKSAND FILTER
	//##########################################	
	
	
	
	
	
	// get the initial (full) list
	
	var $filterList = $('ul#portfolio-list');
		
	// Unique id 
	for(var i=0; i<$('ul#portfolio-list li').length; i++){
		$('ul#portfolio-list li:eq(' + i + ')').attr('id','unique_item' + i);
	}
	
	// clone list
	var $data = $filterList.clone();
	
	
	// Click
	$('#portfolio-filter a').click(function(e) {
		if($(this).attr('rel') == 'all') {
			// get a group of all items
			var $filteredData = $data.find('li');
		} else {
			// get a group of items of a particular class
			var $filteredData = $data.find('li.' + $(this).attr('rel'));
		}
		
		// call Quicksand
		$('ul#portfolio-list').quicksand($filteredData, {
			duration: 500,
			attribute: function(v) {
				// this is the unique id attribute we created above
				return $(v).attr('id');
			}
		}, function() {
	        // restart functions
	        galleryRestart();
		});
		// remove # link
		e.preventDefault();
	});
	
    
    // set the description from the image at the description holder
    function setImageDescription(title, desc){
    	$('#image-description .title').text(title);
    	$('#image-description .desc').text(desc);
    	return false;
    }
    
	galleryRestart();
	
	
	function galleryRestart(){
		 
	    
	    // open image
	    $("#portfolio-list a").click(function(){
	    
	    	// if not prettyPhoto
	    	if($(this).attr('rel') != "prettyPhoto" ){
	    
		    	// set description
				img_title = $(this).attr('title');
				img_desc = $(this).children('img').attr('alt');
				setImageDescription(img_title, img_desc);
				
				// show
				$("#image-buttons").show();
				
				// hide
				$('#nav').hide();
				$("#gallery-holder").hide();
				$('#bg').hide('');
				
				// put loader image
				$('#no-bg-click').addClass('loading-img');
				
				// load image on Bg and call resizeBg
				var sr = $(this).attr('href');
				imgLoader(sr);
				return false;
			}// if not prettyPhoto
		});
		
		// tooltip
		 $('.gallery-thumbs img').poshytip({
	    	className: 'tip-twitter',
			showTimeout: 1,
			alignTo: 'target',
			alignX: 'center',
			offsetY: 5,
			allowTipHover: false
	    });
	    
	    // prettyPhoto restart
	    $("a[rel^='prettyPhoto']").prettyPhoto();
	}
	
	
	
	//##########################################
	// On load page
	//##########################################

	$(window).load(function(){
		// show scroller
		$('#scroll-holder').fadeIn();
	
		starScrolling();
		
		// Center and resize after all page is loaded
		centerScroll();
		resizeBg();
		fixFooterBottom();
		
		// Hide footer at first
		footerContainerHeight = footerContainer.height() + 3;
		footerContainer.animate({
			marginBottom : -footerContainerHeight
		}, 1, 'easeOutExpo');
		
				
	});
	


});

// search clearance	
function defaultInput(target){
	if((target).value == 'Search...'){(target).value=''}
}

function clearInput(target){
	if((target).value == ''){(target).value='Search...'}
}

// Skin changer (for demo only)

function changeSkin(skin){
	document.getElementById('css-skins').href = 'skins/'+skin+'.css';
	
	if(skin == "dark"){
		logo = 'img/logo-dark.png';
	}else{
		logo = 'img/logo.png';
	}
	document.getElementById('logo').src = logo;
	
}
