(function($) {
	$(document).ready(function() { 
		// Select the user id 
		$("#search_button").click(function() {
			var uid = parseInt( $("#search_text").val() )
			if (uid > 0 && uid < 60) {
				window.location.replace("no-sidebar.html?uid="+uid)
			}
		})

		// Get url query key-value pair
		var params = {};
		document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
		function decode(s) {
		    return decodeURIComponent(s).replace(/\+/g, " ");
		}
		params[decode(arguments[1])] = decode(arguments[2]);
		});

		var colorTheme = [
		  '#ce3440', '#7e42a6', '#bc0a13', '#4362a7', '#ca8f57', '#4ba894', '#4ba894', '#b95c28', '#638db2', '#dbcc58', '#1b3c69', '#d5a753'
		]

		if (parseInt(params.uid) > 0) {
			$.get( "api/recommendation", { uid: params.uid }, function( data ) {
				data = JSON.parse(data)
			  // Update the recommended users name
				$(".user-name").each(function(i, v){
					$(v).text( data.users[i] )
				})
				$(".rest-name").each(function(i, v){
					$(v).text( data.business[i] )
				})

				var width = window.innerWidth * 0.9 
				$("#cloud").css({
					"width": width
				})
				// Show the word cloud
				WordCloud(document.getElementById('cloud'), { 
					list: data.taste,
					gridSize: 10,
		      fontFamily: 'Finger Paint, cursive, sans-serif',
		      color: function() { return colorTheme[Math.floor(Math.random() * colorTheme.length)] },
		      shuffle: true,
		      drawOutOfBound: false,
		      rotateRatio: 0,
		      ellipticity: 0.3,
		      backgroundColor: 'transparent'
				} );	
			});
		}
	});  
})(jQuery);