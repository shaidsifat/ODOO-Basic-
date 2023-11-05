function printInvoice(orderId,divId) {
      const queryParams = new URLSearchParams(window.location.search);
      const queryDict = {};
      for (const [key, value] of queryParams.entries()) {
        queryDict[key] = value;
      }
      menuId = queryDict.menu_id
      actionId = queryDict.action
      SaleOrderId = queryDict.id
      var printContents = document.getElementById(divId).innerHTML;
      var originalContents = document.body.innerHTML;
      document.body.innerHTML = printContents;
      window.print();
      document.body.innerHTML = originalContents;
      window.setTimeout(function() {
        window.close();
      }, 2000);
      url = "/web#view_type=form&model=sale.order&menu_id=" + menuId + "&action=" + actionId;
      window.opener.location.href = url
      window.opener.location.reload();
 };