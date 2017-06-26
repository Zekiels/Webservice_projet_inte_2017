$("#connec").click(function(){

			$.ajax("http://limonade-equipe7.herokuapp.com/idGet").done(function(data){
				//debugger;
				$("#name").text(data);
			});
		});


$("#creat").click(function(){

			str=JSON.stringify($('#name').val());

			console.log(str)
			$.ajax({
  				type: "POST",
				url: "http://limonade-equipe7.herokuapp.com/idPost",
  				data: str,
  				dataType: 'text'
			});
		});

$("#connec").click(function(){

			str=JSON.stringify($('#name').val());

			console.log(str)
			$.ajax({
  				type: "POST",
				url: "http://limonade-equipe7.herokuapp.com/idIsValide",
  				data: str,
  				dataType: 'text'
			});
		});
