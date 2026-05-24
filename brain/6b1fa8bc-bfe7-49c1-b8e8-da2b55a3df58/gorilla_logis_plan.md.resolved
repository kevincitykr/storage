# Gorilla Logis Shipping Management Plan

This plan outlines how to collect and manage shipping order data from the Gorilla Logis "My Page" service list.

## 1. Data Schema
Each order will be stored with the following fields:
- `gr_no`: The main order number (e.g., GR2604222077764)
- `tracking_no`: The domestic/international tracking number
- `item_name`: Representative item name
- `recipient`: Name of the consignee (e.g., 손효정)
- `weight`: Measured weight in kg
- `cost_krw`: Shipping cost in KRW
- `status`: Current status (e.g., 출고완료, 입고대기)
- `order_date`: Date the order was placed
- `updated_at`: Timestamp of last local update

## 2. Management Workflow
1.  **Extract**: User runs a JS snippet in the browser console to copy order data.
2.  **Store**: Data is saved to `gorilla_orders.json` via a Python management script.
3.  **Track**: The Python script allows searching by recipient or tracking number and alerts for status changes.

## 3. Component List
- `extract_gorilla.js`: Script to be run in the browser console.
- `gorilla_manager.py`: Python CLI tool to ingest, list, and filter orders.
- `gorilla_orders.json`: Local database file.
