async function select_bill_no(){
    
    detail_or_update=document.getElementById("detail_or_update");
    if(detail_or_update.value==="1")
    {
    return;
    }
    axios({
        method:"GET",
        url:'/bill/select_bill_no/',
        headers:{'Content-type':'application/json','X-CSRFToken':getCookie("csrftoken")}
    }).then(response=>{
        if(response.status==200 || response.status==201){
            // console.log("response.data ",response.data," response.data[0] ",response.data['bill_no'])
            bill_no=document.getElementById("bill_no");
            bill_no_span=document.getElementById("bill_no_span");
            bill_no.value=response.data['bill_no'];
            // document.getElementById("bill_no").value=response.data[0]['bill_no']
            bill_no_span.innerHTML=response.data['bill_no'];           
        }
    })
}

select_bill_no()