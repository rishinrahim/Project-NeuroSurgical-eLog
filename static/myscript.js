function curdate()
{				var currentDate = new Date()
			    var day = currentDate.getDate()
			    var month = currentDate.getMonth();
			    var year = currentDate.getFullYear();
				var n = currentDate.getDay();
				weekday = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');
			    monthw=new Array('January', 'February', 'March', 'April', 'May', 'June', 'July' ,'August' ,'September','October', 'November', 'December');
			    document.getElementById('date').innerHTML = day+" "+monthw[month]+" "+year+" "+weekday[n];
}

$(document).ready(function(){

	curdate();
	})
	
  $(document).ready(function(){
	
	$('#datepicker').datepicker({
	dateFormat: "dd/mm/yy",
	});
	$('#start').timepicker();
	$('#end').timepicker();
	
	})
	