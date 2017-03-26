module.exports = [
    {
        api_string: '/api/mme_query', 
        program: 'python.exe ',
        script: 'scripts/PM_statis_report_mysql.py',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        program: 'python.exe ',
        script: 'scripts/SAEGW_statis_mysql.py',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query', 
        program: 'python.exe ',
        script: 'scripts/PM_statis_report_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        program: 'python.exe ',
        script: 'scripts/SAEGW_statis_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    }
]
