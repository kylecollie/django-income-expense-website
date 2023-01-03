const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const tableBody = document.querySelector('.table-body');
const paginationContainer = document.querySelector('.pagination-container');

tableOutput.style.display = 'none';

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    console.log('>>> searchValue: ', searchValue);

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = 'none';
        tableBody.innerHTML = '';

        fetch("/income/search-income", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                appTable.style.display = 'none';
                tableOutput.style.display = 'block';
                if (data.length === 0) {
                    tableOutput.innerHTML = 'No results found';
                } else {
                    data.forEach(item => {
                        tableBody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.source}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        </tr>
                        `
                    });
                }
            });
        } else {
            tableOutput.style.display = 'none';
            appTable.style.display = 'block';
            paginationContainer.style.display = 'block';
        }
});
