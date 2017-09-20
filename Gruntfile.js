// Project configuration.
module.exports = function(grunt) {
    grunt.initConfig({
        //pkg: grunt.file.readJSON('package.json'),
        clean: {
            coverage: {
                src: ['coverage/']
            }
        },
        copy: {
            coverage: {
                src: ['tests/**', 'src/**'],
                dest: 'coverage/'
            }
        },
        //grunt-blanket too outmoded, enve not kown token 'const' 
        //blanket: {
        //    coverage: {
        //        src: ['src/'],
        //        dest: 'coverage/src/'
        //    }
        //},
        
        mochaTest: {
            test: {
                options: {
                    reporter: 'spec',
                    captureFile: 'tests/output/results.txt', // Optionally capture the reporter output to a file
                    quiet: false, // Optionally suppress output to standard out (defaults to false)
                    clearRequireCache: false, // Optionally clear the require cache before running tests (defaults to false)
                    noFail: false, // Optionally set to not fail on failed tests (will still fail on other errors)
                    //require: [
                    //    'babel-register'
                        //'coverage/blanket'
                    //]
                },
                src: ['coverage/tests/**/*.js'],
                //dest: './tests/output/mocha_xunit.out',
            },
            //'html-cov': {
            //    options: {
            //        reporter: 'html-file-cov',
            //        // use the quiet flag to suppress the mocha console output
            //        quiet: false,
            //        // specify a destination file to capture the mocha
            //        // output (the quiet option does not suppress this)
            //        captureFile: 'coverage.html'
            //    },
            //    src: ['coverage/tests/**/*.js']
            //}
            // The travis-cov reporter will fail the tests if the
            // coverage falls below the threshold configured in package.json
            // because the grunt-blanket is too outmoded, give up the coverage test
            //'travis-cov': {
            //    options: {
            //    reporter: 'travis-cov'
            //    },
            //    src: ['coverage/tests/**/*.js']
            //}
        },
    });

    
    // A very basic default task.
    grunt.registerTask('default', ['clean', 'copy', 'mochaTest']);

    // Add the grunt-mocha-test tasks.
    grunt.loadNpmTasks('grunt-mocha-test');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');
    //grunt.loadNpmTasks('grunt-blanket');
        
    //grunt.loadNpmTasks('mocha-html-cov-reporter');
}