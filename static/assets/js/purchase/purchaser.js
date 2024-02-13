
async function show_purchaser(id=null)
{
    
    // alert("called purchaser_show")
    id='all'
    let url=`/purchase/purchasers/${id}/`
    purchaser=document.getElementById("purchaser");
    let response=await axios({
            method:"GET",
            url:url,
            headers:{'type':'application/json','X-CSRFToken':getCookie("csrftoken")}
        });
    // console.log("response.data=",response.data)
    return response.data;
}



async function create_purchasers()
{
    // console.log("purchaser ",response)
    var data_dict=await show_purchaser()
    // console.log("data_dict ",data_dict)
    for(let key in data_dict)
    {
        var label=data_dict[key]['name'];
        var value=data_dict[key]['id'];
        var name=null;
        var id=null
        // console.log("id====",id)
        const element=await create_element(type="option",id,name,value,label,isrequired=false)
        // console.log("element=",element)
        document.getElementById("purchaser").appendChild(element)
    }
}