/* **************************************************************
File: mock.js
Library to provide mock api responses.
* **************************************************************/
 
'use strict';

function getUser() {
  console.log("Message from 'getUser method in mock.js' :)");
  
  let user = {
    username: "MockUser",
    role: "Regular",
    loggedIn: true,
    error: null
  };
  
  return Promise.resolve(user);
}

function getPaginatedAssetsMock(link='/assets/0') {
  // debug:
  console.log("Message from 'getPaginatedAssetsMock method in mock.js' :)");
  return Promise.resolve(
    // return assets listing object, as specified by the backend api   
    {
      "data": {
	    "assets": {
		"1": {"asset_id": "000001",
			 "bulk_count": 1,
			 "bulk_count_removed": 0,
			 "category_1": "AC",
			 "category_2": null,
			 "cost": 1000.25,
			 "cost_brand_new": 1000.25,
			 "date_placed": "2019-01-01 15:00:01",
			 "date_removed": null,
			 "date_warranty_expires": "2020-03-25 00:00:00",
			 "description": "test 1",
			 "far": [],
			 "id": 1,
			 "invoices": [{"asset_amount": 100.0,
				       "file_path": "https://picsum.photos/200/300",
				       "id": 1,
				       "notes": "Testing invoice 1",
				       "number": "100",
				       "total": 100.0},
				      {"asset_amount": 50.0,
				       "file_path": "https://picsum.photos/200/300",
				       "id": 2,
				       "notes": "Testing invoice 2",
				       "number": "200",
				       "total": 200.0}],
			 "is_current": true,
			 "life_expectancy_years": 8,
			 "location_counts": [],
			 "manufacturer": "Carrier",
			 "model_number": "38KCE009118",
			 "pictures": ["https://picsum.photos/id/0/200/300",
				      "https://picsum.photos/id/24/200/300",
				      "https://picsum.photos/id/26/200/300"],
			 "receiving": "shipped",
			 "requisition": "donated",
			 "serial_number": "1302770188",
			 "shipping": 20.0,
			 "supplier": "Island Breeze"},

		   "2": {"asset_id": "000002",
			 "bulk_count": 1,
			 "bulk_count_removed": 0,
			 "category_1": "AC",
			 "category_2": "Vehicles",
			 "cost": 500.0,
			 "cost_brand_new": 500.0,
			 "date_placed": "2019-01-01 15:00:01",
			 "date_removed": null,
			 "date_warranty_expires": null,
			 "description": "test 2 - far 1",
			 "far": [{"account_description": "test account 1",
				  "account_id": 1,
				  "account_number": "60261",
				  "amount": 2000.0,
				  "description": "test far 1",
				  "id": 1,
				  "life": 5,
				  "pdf": 100,
				  "start_date": "2020-02-02 00:00:00"}],
			 "id": 2,
			 "invoices": [{"asset_amount": 250.0,
				       "file_path": "",
				       "id": 3,
				       "notes": "Testing invoice 3",
				       "number": "300",
				       "total": 250.0},
				      {"asset_amount": 250.0,
				       "file_path": "https://picsum.photos/200/300",
				       "id": 4,
				       "notes": "Testing invoice 4",
				       "number": "400",
				       "total": 250.0}],
			 "is_current": true,
			 "life_expectancy_years": null,
			 "location_counts": [{"audit_date": null,
					      "count": 1,
					      "count_id": 1,
					      "description": "root",
					      "location_id": 1,
					      "parent_id": null}],
			 "manufacturer": "Carrier",
			 "model_number": "15KCE009119",
			 "pictures": ["https://picsum.photos/200/300"],
			 "receiving": "received",
			 "requisition": "unspecified",
			 "serial_number": "1302770189",
			 "shipping": null,
			 "supplier": "Island Breeze"},

		   "3": {"asset_id": "000003",
			 "bulk_count": 3,
			 "bulk_count_removed": 0,
			 "category_1": "AC",
			 "category_2": null,
			 "cost": 1000.0,
			 "cost_brand_new": 1000.0,
			 "date_placed": "2019-01-01 15:00:01",
			 "date_removed": null,
			 "date_warranty_expires": null,
			 "description": "test 3 - far 2",
			 "far": [{"account_description": "test account 2",
				  "account_id": 2,
				  "account_number": "60262",
				  "amount": 4000.61,
				  "description": "test far 2",
				  "id": 2,
				  "life": 8,
				  "pdf": 101,
				  "start_date": "2000-02-02 00:00:00"}],
			 "id": 3,
			 "invoices": [{"asset_amount": 500.0,
				       "file_path": "https://picsum.photos/200/300",
				       "id": 5,
				       "notes": "Testing invoice 5",
				       "number": "500",
				       "total": 500.0}],
			 "is_current": true,
			 "life_expectancy_years": 8,
			 "location_counts": [{"audit_date": null,
					      "count": 1,
					      "count_id": 2,
					      "description": "subB",
					      "location_id": 3,
					      "parent_id": 1},
					     {"audit_date": "2020-03-24 13:00:00",
					      "count": 2,
					      "count_id": 3,
					      "description": "subB-2",
					      "location_id": 6,
					      "parent_id": 3}],
			 "manufacturer": "Carrier",
			 "model_number": "38KCE009118",
			 "pictures": ["https://picsum.photos/200/300"],
			 "receiving": "placed",
			 "requisition": "partial payment",
			 "serial_number": "1302770188",
			 "shipping": null,
			 "supplier": "Island Breeze"},

		   "4": {"asset_id": "000004",
			 "bulk_count": 1,
			 "bulk_count_removed": 0,
			 "category_1": "AC",
			 "category_2": null,
			 "cost": 500.0,
			 "cost_brand_new": 500.0,
			 "date_placed": "2019-01-01 15:00:01",
			 "date_removed": null,
			 "date_warranty_expires": null,
			 "description": "test 4",
			 "far": [],
			 "id": 4,
			 "invoices": [{"asset_amount": 50.0,
				       "file_path": "https://picsum.photos/200/300",
				       "id": 6,
				       "notes": "Testing invoice 6",
				       "number": "600",
				       "total": 500.0}],
			 "is_current": true,
			 "life_expectancy_years": 8,
			 "location_counts": [],
			 "manufacturer": "Carrier",
			 "model_number": "15KCE009119",
			 "pictures": [],
			 "receiving": "unspecified",
			 "requisition": "unspecified",
			 "serial_number": "1302770189",
			 "shipping": null,
			 "supplier": "Island Breeze"},

		   "5": {"asset_id": "000005",
			 "bulk_count": 1,
			 "bulk_count_removed": 0,
			 "category_1": "AC",
			 "category_2": null,
			 "cost": 1000.0,
			 "cost_brand_new": 1000.0,
			 "date_placed": "2019-01-01 15:00:01",
			 "date_removed": null,
			 "date_warranty_expires": null,
			 "description": "test 5",
			 "far": [],
			 "id": 5,
			 "invoices": [{"asset_amount": 1000.0,
				       "file_path": "https://picsum.photos/200/300",
				       "id": 7,
				       "notes": "Testing invoice 7",
				       "number": "700",
				       "total": 5000.0}],
			 "is_current": true,
			 "life_expectancy_years": 8,
			 "location_counts": [],
			 "manufacturer": "Carrier",
			 "model_number": "38KCE009118",
			 "pictures": [],
			 "receiving": "placed",
			 "requisition": "paid in full",
			 "serial_number": "1302770188",
			 "shipping": null,
			 "supplier": "Island Breeze"}}
	},

	 "filters": {"asset.cost__gt": null,
		     "asset.cost__lt": null,
		     "asset.description__contains": null,
		     "location": null},
	 "msg": "testing",
	 "next": "/assets/1"
    } // end object passed to Promise.resolve method 
  );
}


function getAllLocationsMock() {
  // debug:
  console.log("Message from 'getAllLocationsMock method in mock.js' :)");
  return Promise.resolve(
    {

      'data':{
        'locations':{
          '1': {
            'description': 'root',
            'parent': null
          },
          '2': {
            'description': 'subA',
            'parent': 1
          },
          '3': {
            'description': 'subB',
            'parent': 1
          },
          '4': {
            'description': 'subA-1',
            'parent': 2
          },
          '5': {
            'description': 'subB-1',
            'parent': 3
          },
          '6': {
            'description': 'subB-2',
            'parent': 3
          }
        }
      }

    }
  );
}
      //var file_access_token = provider.getTokensFromStorage().file_access_token
function getTokensFromStorage() {
  console.log("Message from 'getAllLocationsMock method in mock.js' :)");
  return Promise.resolve({
    'file_access_token':'testfileaccesstoken',
  });
}

export default {
  getUser,
  getPaginatedAssetsMock,
  getAllLocationsMock,
  getTokensFromStorage,
}

