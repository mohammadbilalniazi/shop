
async function show_creator(id=null)
{
    call_shirkat
    if(id==null)
    {
        id="all"
    }
    let url=`/purchase/creators/${id}/`
    creator=document.getElementById("creator");
    let response=call_shirkat(url,'GET');
    // console.log("creator.data=",response.data)
    return response.data;
}



async function create_creators()
{
    // console.log("creator ",response)
    var data_dict=await show_creator()
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
        document.getElementById("creator").appendChild(element)
    }
}