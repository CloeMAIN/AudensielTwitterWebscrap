import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Dropdown } from 'semantic-ui-react'; // Import des composants Semantic UI React
import { useTable, usePagination, useFilters } from 'react-table';

function ReqTable() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        const response = await axios.get('http://localhost:8000/api/display_req');
        //const response = await axios.get('https://scrappertwitter.pythonanywhere.com/api/display_req');
        
        setData(response.data);
        setLoading(false);
    };

    useEffect(() => {
        fetchData();
    }, []);

    const rerunRequest = async (reqId) => {
        try {
            const response = await axios.get(`http://localhost:8000/api/display_req/${reqId}`);
            const request = response.data;
            const mot_cle = request.mot_cle;
            const date_debut = request.date_debut;
            const date_fin = request.date_fin;
            const nb_tweets = request.nb_tweets;
            await axios.get(`http://localhost:8000/api/search/${mot_cle}/${date_fin}/${date_debut}/${nb_tweets}`);
            // Handle success or display a message
            console.log('Request rerun successfully');
        } catch (error) {
            console.error('Error rerunning request:', error);
        }
    };

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
                Header: 'Actions',
                accessor: 'actions',
                Cell: ({ row }) => (
                    <Button onClick={() => rerunRequest(row.original.req_id)}>Rerun</Button>
                ),
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
        gotoPage,
        nextPage,
        previousPage,
        setPageSize,
        state: { pageIndex, pageSize },
    } = useTable({ columns, data }, useFilters, usePagination);

    if (loading) return <div>Loading...</div>;

    return (
        <>
            <Table {...getTableProps()} celled>
                <Table.Header>
                    {headerGroups.map(headerGroup => (
                        <Table.Row {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map(column => (
                                <Table.HeaderCell {...column.getHeaderProps()}>{column.render('Header')} </Table.HeaderCell>
                            ))}
                        </Table.Row>
                    ))}
                </Table.Header>
                <Table.Body {...getTableBodyProps()} style={{ width: '90%', height: '60vh', margin: '0 auto', overflowY: 'auto' }} >
                    {page.map(row => {
                        prepareRow(row);
                        return (
                            <Table.Row {...row.getRowProps()}>
                                {row.cells.map(cell => (
                                    <Table.Cell {...cell.getCellProps()} >{cell.render('Cell')}</Table.Cell>
                                ))}
                            </Table.Row>
                        );
                    })}
                </Table.Body>
            </Table>
            <div>
                <Button onClick={() => previousPage()} disabled={!canPreviousPage}>
                    {'<'}
                </Button>
                <Button onClick={() => nextPage()} disabled={!canNextPage}>
                    {'>'}
                </Button>
                <Button onClick={fetchData}>Charger les données</Button>
                <span>
                    Page{' '}
                    <strong>
                        {pageIndex + 1} sur {pageOptions.length}
                    </strong>{' '}
                </span>
                <span>
                    | Aller à la page:{' '}
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
                <Dropdown
                    selection
                    compact
                    value={pageSize}
                    onChange={(e, { value }) => {
                        setPageSize(Number(value));
                    }}
                    options={[
                        { key: 5, text: '5', value: 5 },
                        { key: 10, text: '10', value: 10 },
                        { key: 20, text: '20', value: 20 },
                        { key: 30, text: '30', value: 30 },
                        { key: 40, text: '40', value: 40 },
                        { key: 50, text: '50', value: 50 },
                    ]}
                />
            </div>
        </>
    );
}

export default ReqTable;
