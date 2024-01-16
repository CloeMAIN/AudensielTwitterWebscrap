import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTable, usePagination, useFilters } from 'react-table';

function ReqTable() {
    const [data, setData] = useState([]);

    const fetchData = async () => {
        const response = await axios.get('http://localhost:8000/api/display_req');
        //const response = await axios.get('https://scrappertwitter.pythonanywhere.com/api/display_req');
        
        setData(response.data);
    };

    useEffect(() => {
        fetchData();
    }, []);

    const columns = React.useMemo(
        () => [
            {
                Header: 'Req ID',
                accessor: 'req_id',
            },
            {
                Header: 'Mot Clé',
                accessor: 'mot_cle',
            },
            {
                Header: 'Date Fin',
                accessor: 'date_fin',
            },
            {
                Header: 'Date Debut',
                accessor: 'date_debut',
            },
            {
                Header: 'Nb Tweets',
                accessor: 'nb_tweets',
            },
            {
                Header: 'Last Date Pulled',
                accessor: 'last_date_pulled',
            },
        ],
        []
    );

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        prepareRow,
        page,
        canPreviousPage,
        canNextPage,
        pageOptions,
        pageCount,
        gotoPage,
        nextPage,
        previousPage,
        setPageSize,
        state: { pageIndex, pageSize },
    } = useTable({ columns, data }, useFilters, usePagination);

    return (
        <>
            
            <table {...getTableProps()}>
                <thead>
                    {headerGroups.map(headerGroup => (
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map(column => (
                                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {page.map(row => {
                        prepareRow(row);
                        return (
                            <tr {...row.getRowProps()}>
                                {row.cells.map(cell => (
                                    <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                                ))}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
            <div>
                <button onClick={() => previousPage()} disabled={!canPreviousPage}>
                    {'<'}
                </button>
                <button onClick={() => nextPage()} disabled={!canNextPage}>
                    {'>'}
                </button>
                <button onClick={fetchData}>Charger les données</button>
                <span>
                    Page{' '}
                    <strong>
                        {pageIndex + 1} of {pageOptions.length}
                    </strong>{' '}
                </span>
                <span>
                    | Go to page:{' '}
                    <input
                        type="number"
                        defaultValue={pageIndex + 1}
                        onChange={e => {
                            const page = e.target.value ? Number(e.target.value) - 1 : 0;
                            gotoPage(page);
                        }}
                        style={{ width: '100px' }}
                    />
                </span>{' '}
                <select
                    value={pageSize}
                    onChange={e => {
                        setPageSize(Number(e.target.value));
                    }}
                >
                    {[5,10, 20, 30, 40, 50].map(pageSize => (
                        <option key={pageSize} value={pageSize}>
                            Show {pageSize}
                        </option>
                    ))}
                </select>
            </div>
        </>
    );
}

export default ReqTable;