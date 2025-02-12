{
    "name": "PO from BOM",
    "version": "1.0",
    "category": "Manufacturing",
    "summary": "Create purchase orders from Bill of Materials",
    "description": "This module allows users to create purchase orders based on the components of a Bill of Materials (BoM) and to generate delivery orders for selected customers.",
    "author": "Wildy Estephan",
    "depends": [
        "mrp",
        "purchase",
        "stock"
    ],
    "data": [
        "views/mrp_bom_views.xml",
        "views/select_customer_wizard_views.xml",
    ],
}