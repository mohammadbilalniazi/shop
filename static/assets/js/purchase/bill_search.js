var data;
async function make_table2(data)
{
    if(data['query'].length==0)
    {
        return;
    }

    var keys= Object.keys(data['query'][0])
    // console.log("keys ",keys)
    var columnDefs=[];
    for(key in keys){
           obj_keys= {headerName: keys[key], field: keys[key]}
           columnDefs.push(obj_keys);
    }
    // action_dict
    columnDefs.push({headerName: "Action", field: "action"})
    // console.log("columnDefs=",columnDefs)
    var rowData=data['query'];
    for(key in rowData){    

        var store=await show_store(rowData[key]['store_id']) 
        var creator=await show_creator(rowData[key]['creator_id'])
        var vendor=await show_vendor(rowData[key]['vendor_id'])
        // console.log("vendor=",vendor)
        // 
        rowData[key]['creator_id']=creator[0]['name'];
        rowData[key]['store_id']=store[0]['name'];
        rowData[key]['vendor_id']=vendor[0]['name'];
        var action=`<a href="/bill/update/${rowData[key]['id']}/" class="btn btn-success" role="button">update</a> | <a href="/bill/delete/${rowData[key]['id']}/" role="button" class="btn btn-success">delete</a> | <a href="/bill/detail/${rowData[key]['id']}/" role="button" class="btn btn-info">Detail</a>`;
        // var doc=new DOMParser().parseFromString(action, "text/xml")
        const spanElement = document.createElement('span');
        spanElement.innerHTML = action;
        rowData[key]['action']=spanElement;
    }
    // // return;
    var gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData
    };
    // var columnDefs = [
    //     {headerName: "Make", field: "make"},
    //     {headerName: "Model", field: "model"},
    //     {headerName: "Price", field: "price"}
    //   ];
          
    //   // specify the data
    //   var rowData = [
    //     {make: "Toyota", model: "Celica", price: 35000},
    //     {make: "Ford", model: "Mondeo", price: 32000},
    //     {make: "Porsche", model: "Boxter", price: 72000}
    //   ];
    var gridDiv = document.querySelector('#myGrid');
    gridDiv.innerHTML="";
    new agGrid.Grid(gridDiv, gridOptions);
    // });
    return;
}

async function make_table(data)
{
    const bill_tbody = document.querySelector('#bill_tbody');
    majmoa_upon_shirkat=document.getElementById("majmoa_upon_shirkat");
    majmoa_upon_shirkat.value=data.statistics.majmoa_upon_shirkat;
    majmoa_upon_rcvr_org=document.getElementById("majmoa_upon_rcvr_org");
    majmoa_upon_rcvr_org.value=data.statistics.majmoa_upon_rcvr_org;
    majmoa_baqaya=document.getElementById("majmoa_baqaya");
    majmoa_baqaya.value=data.statistics.majmoa_baqaya;
    if(majmoa_baqaya.value<0)
    {
     majmoa_baqaya.style.color="black";
     majmoa_baqaya.style.background="red";
    }
    else
    {
        
     majmoa_baqaya.style.color="black";
     majmoa_baqaya.style.background="green";
    }

    total_sum_purchase=document.getElementById("total_sum_purchase");
    total_sum_purchase.value=data.statistics.total_sum_purchase;
    payment_sum_purchase=document.getElementById("payment_sum_purchase");
    payment_sum_purchase.value=data.statistics.payment_sum_purchase;
    baqaya_purchase=document.getElementById("baqaya_purchase");
    baqaya_purchase.value=data.statistics.baqaya_purchase;

    total_sum_selling=document.getElementById("total_sum_selling");
    total_sum_selling.value=data.statistics.total_sum_selling;
    payment_sum_selling=document.getElementById("payment_sum_selling");
    payment_sum_selling.value=data.statistics.payment_sum_selling;
    baqaya_selling=document.getElementById("baqaya_selling");
    baqaya_selling.value=data.statistics.baqaya_selling;
    console.log("data.statistics.baqaya_selling ",data.statistics.baqaya_selling)

    
    total_sum_payment=document.getElementById("total_sum_payment");
    total_sum_payment.value=data.statistics.total_sum_payment;
    payment_sum_payment=document.getElementById("payment_sum_payment");
    payment_sum_payment.value=data.statistics.payment_sum_payment;

    total_sum_receivement=document.getElementById("total_sum_receivement");
    total_sum_receivement.value=data.statistics.total_sum_receivement;
    receivement_sum=document.getElementById("receivement_sum");
    receivement_sum.value=data.statistics.payment_sum_receivement;
    
    total_sum_expense=document.getElementById("total_sum_expense");
    total_sum_expense.value=data.statistics.total_sum_expense;
    payment_sum_expense=document.getElementById("payment_sum_expense");
    payment_sum_expense.value=data.statistics.payment_sum_expense;
    bill_tbody.innerHTML="";
    // console.log(data)
    class Bills
    {
        constructor(no,
            id,
            bill_type,
            organization_id,
            store_id,
            bill_no,
            creator_id,
            rcvr_org,
            total,
            payment,
            discount,
            date
            ) {
        this.no = no;
        this.id=id;
        this.bill_type=bill_type;
        this.organization=organization_id;
        this.store=store_id; 
        this.bill_no = bill_no;
        this.creator=creator_id;
        this.rcvr_org=rcvr_org; 
        this.total=total;
        
        this.payment=payment;
        this.discount=discount;
        this.date=date;
        }

        addHtml() {
            let row=`
                <tr>
                  <td>${this.store}</td><td>${this.bill_no}(<span style="color:green;font-weight:600">${this.bill_type}</span>)</td>
                    <td>${this.rcvr_org}</td><td>${this.total}</td>
                    <td>${this.payment}</td><td>${this.date}</td>
                    <td> <a href="/bill/update/${this.id}/" class="btn btn-success" role="button">update</a> | <a href="/bill/delete/${this.id}/" role="button" class="btn btn-success">delete</a> | <a href="/bill/detail/${this.id}/" role="button" class="btn btn-info">Detail</a>
                    </td>
                </tr>`;
             
                bill_tbody.insertAdjacentHTML('beforeend', row);
        }
    }
    let bills_list = [];
    
    for(key in data['query']){    

        // var store=await show_store(data['query'][key]['store_id']) 
        var store=data['query'][key]['store_id']
        // var creator=await show_creator(data['query'][key]['creator_id'])
        var creator=data['query'][key]['creator_id']
        console.log("data['query'][key]=",data['query'][key])
        // var vendor=await show_vendor(data['query'][key]['vendor_id'])
        var rcvr_org=data['query'][key]['rcvr_org']
        // alert(creator)
        console.log("vendor ",rcvr_org," store ",store," creator ",data['query'][key]['creator_id']);
        bills_list.push(new Bills(key,data['query'][key]['id'],
                                data['query'][key]['bill_type'],
                                data['query'][key]['organization_id'],
                                // store[0]['name'],
                                store,
                                data['query'][key]['bill_no'],
                                creator,
                                // vendor[0]['name'],
                                rcvr_org,
                                data['query'][key]['total'],                   
                                data['query'][key]['payment'],
                                data['query'][key]['discount'],
                                data['query'][key]['date'],
                             ))
        // console.log("data ",data,"data['bill_no'] ",data['bill_no'])
    }
    bills_list.forEach(mudeeriath=>mudeeriath.addHtml());
}
function search_purchase()
{
    var start_date=document.getElementById("start_date_input").value;
    var end_date=document.getElementById("end_date_input").value;
    var bill_no=document.getElementById("bill_no").value;
    var creator=document.getElementById("creator").value;
    var rcvr_org=document.getElementById("rcvr_org").value;
    
    var bill_type=document.getElementById("bill_type").value;
    if(bill_no=="" || bill_no==null)
    {
        bill_no=0;
    }

    if(rcvr_org=="")
    {
        rcvr_org="all";
    }

    if(creator=="")
    {
        creator="all";
    }
    // alert("purchase_detail_delete")

    axios({
        method:"GET",   
        url:`/bill/search/${bill_type}/${parseInt(bill_no)}/${rcvr_org}/${creator}/${start_date}/${end_date}`,   
        headers:{"Content-Type":"application/json","X-CSRFToken":getCookie('csrftoken')}
        
    }).then((response)=>{
        console.log("response ",response.data);
       make_table(response.data);
    });
}


document.getElementById("bill_no").addEventListener("input",e=>{search_purchase();});

document.getElementById("rcvr_org").addEventListener("input",e=>{search_purchase();});

document.getElementById("creator").addEventListener("input",e=>{search_purchase();});

document.getElementById("bill_type").addEventListener("change",e=>{search_purchase();});
// document.getElementById("start_date_input").addEventListener("change",e=>{search_purchase();});

// document.getElementById("end_date_input").addEventListener("change",e=>{search_purchase();});
function date_change()
{
    search_purchase();
}
search_purchase();