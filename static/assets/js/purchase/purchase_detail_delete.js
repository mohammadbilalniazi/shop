function purchase_detail_delete(bill_detail_id)
{
    bill_no=document.getElementById("bill_no").value;
    // alert("purchase_detail_delete")
    // console.log("bill_detail_id=",bill_detail_id," bill_no ",bill_no)
    // return false;
    // console.log("csrftoken ",csrftoken)
    axios({
        method:"DELETE",   
        url:`/bill/detail/delete/${bill_no}/${bill_detail_id}`,   
        headers:{"Content-Type":"application/json","X-CSRFToken":getCookie('csrftoken')}
    }).then((response)=>{
        console.log("re ",response.status);
    });
}