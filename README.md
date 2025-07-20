# tds_roe

Repo for collaboration

# Tools:

https://json-table-correlation.streamlit.app/

https://table-data-from-pdf.streamlit.app/

# Helper Scripts

Run in console to enable all input elements

```JS
const inputs = document.querySelectorAll('input');
const textboxes = document.querySelectorAll('textarea');
const buttons  = document.querySelectorAll('button');

// Enable all inputs
inputs.forEach(input => input.removeAttribute('disabled'));

// Enable all buttons
buttons.forEach(button => button.removeAttribute('disabled'));

// Enable and show all textareas
textboxes.forEach(textarea => {
  textarea.removeAttribute('disabled');
  textarea.classList.remove('d-none');
  textarea.style.visibility = 'visible';
  textarea.style.display = 'block';


  // Remove inline styles that hide interactivity or visibility
  textarea.style.opacity = '1';
  textarea.style.pointerEvents = 'auto';
});
```

Run in console to extract tables in excel_tables.xlsx

```JS
/**
 * Scans the page for all tables and downloads them as an Excel (.xlsx) file,
 * with each table placed on a separate sheet.
 * This script dynamically loads the SheetJS (xlsx) library.
 */
(async function() {
    // 1. Load the SheetJS library from a CDN
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js";
    document.head.appendChild(script);

    console.log("Loading SheetJS library...");

    // Wait for the script to load
    await new Promise(resolve => script.onload = resolve);

    console.log("SheetJS loaded. Finding tables...");

    // 2. Find all table elements
    const tables = document.querySelectorAll('table');
    if (tables.length === 0) {
        console.log("No tables found on this page. 🤔");
        return;
    }

    console.log(`Found ${tables.length} table(s). Creating Excel workbook...`);

    // 3. Create a new workbook and add each table as a sheet
    const wb = XLSX.utils.book_new(); // Create a new workbook
    tables.forEach((table, index) => {
        // Convert the HTML table element directly to a worksheet
        const ws = XLSX.utils.table_to_sheet(table);
        // Add the worksheet to the workbook with a name like "Sheet 1", "Sheet 2", etc.
        XLSX.utils.book_append_sheet(wb, ws, `Table ${index + 1}`);
    });

    // 4. Trigger the download of the .xlsx file
    XLSX.writeFile(wb, "excel_tables.xlsx");
    console.log("Excel file with multiple sheets downloaded successfully! ✨");
})();
```
