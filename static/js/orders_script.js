window.onload = function () {
    
    
    
    
    orderSummaryUpdate()
    
    document.querySelectorAll('input[type="number"]').forEach(elem => {
        elem.addEventListener('change', () => {
            orderSummaryUpdate()
        })
    })
    
    document.querySelectorAll('input[type="checkbox"]').forEach(elem => {
        elem.addEventListener('change', () => {
            orderSummaryUpdate()
        })
    })
    
    document.querySelectorAll('select').forEach(elem => {
        elem.addEventListener('change', getPrice)
    })

    function getPrice() {
        let target = event.target
        let index = parseInt(target.name.replace('orderitems-', '').replace('-product', ''))
        const product_id = this.options[this.selectedIndex].value
        const hostname = window.location.host
        if (product_id) {
            let url = `http://${hostname}/api/product?id=${product_id}`
            fetch(url)
                .then(response => response.json())
                .then(json => {
                    priceUpdate(index, parseFloat(json.price || 0))
                })
                .catch(err => { console.log(err) })
        } else {
            priceUpdate(index, 0)
        }
        orderSummaryUpdate()
    }
    
    function priceUpdate(index, price) {
        let price_name = `orderitems-${index}-price`
        let quantity_name = `orderitems-${index}-quantity`
        const price_view = document.querySelector(`input[name="${price_name}"]`)
        if (price_view) {
            price_view.value = price.toFixed(2)
            document.querySelector(`input[name="${quantity_name}"]`).value = 0
        }
    }
    
    function orderSummaryUpdate() {
        let quantity_arr = []
        let price_arr = []
        let total_forms = parseInt(document.querySelector('input[name="orderitems-TOTAL_FORMS"]').value)
        const order_total_quantity_view = document.querySelector('.order_total_cost')
        const order_total_cost_view = document.querySelector('.order_total_cost')
        
        
        let order_total_quantity = 0
        let order_total_cost = 0

        for (let i=0; i < total_forms; i++) {
            // let delete_checked = document.querySelector(`input[name="orderitems-${i}-DELETE"]`).checked
            // if (!delete_checked) {
                let quantity = parseInt(document.querySelector('input[name="orderitems-' + i + '-quantity"]').value)
                let price = parseFloat(document.querySelector('input[name="orderitems-' + i + '-price"]').value)
                quantity_arr[i] = quantity || 0
                price_arr[i] = price || 0
            // } else {
            //     quantity_arr[i] = 0
            // }
        }
        
        order_total_quantity = quantity_arr.reduce((a,b) => a + b, 0)
        order_total_cost = quantity_arr.reduce((a,b,i) => a + (b * price_arr[i]), 0)
        if (order_total_quantity_view) {
            order_total_quantity_view.innerHTML = order_total_quantity
        }
        if (order_total_cost_view) {
            order_total_cost_view.innerHTML = order_total_cost.toFixed(2)
        }
    }

    $('.formset_row').formset({
        addText: 'Add product',
        deleteText: 'Delete',
        prefix: 'orderitems',
        added: addOrderItem,
        removed: deleteOrderItem,
    })

    function addOrderItem(row) {
        console.log('add', row)
        row[0].querySelector('select').addEventListener('change', getPrice)
        row[0].querySelector('input[type="number"]').addEventListener('change', orderSummaryUpdate)
        orderSummaryUpdate()
    }

    function deleteOrderItem(row) {
        console.log('delete', row)
        let target_name= row[0].querySelector('input[type="number"]').name
        let index = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''))
        priceUpdate(index, 0)
        orderSummaryUpdate()
    }
}