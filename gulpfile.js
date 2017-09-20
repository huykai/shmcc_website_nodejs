var gulp = require('gulp');
var del = require('del');
var vinylPaths = require('vinyl-paths');
var mocha = require('gulp-mocha');
var gutil = require('gulp-util');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var changed = require('gulp-changed');
var jscs = require('gulp-jscs');

var SRC = 'src/**/*.js';
var DEST = 'build/';

gulp.task('clean:mobile', function(cb){
    del(['src/log/test_gulp.log'], cb);
});
gulp.task('clean:tmp', function(){
    return gulp.src('tmp/*.js')
    .pipe(vinylPaths(del));
});
gulp.task('mocha', function(){
    return gulp.src(['tests/unit/*.test.js'], {read:false})
    .pipe(mocha({
        reporter: 'spec',
        //globals: {
        //    should: require('should')
        //}
    }))
    .on('error', gutil.log);
});
gulp.task('watch-mocha', function(){
    gulp.watch(['src/**/*.js','tests/unit/*.test.js'],['mocha']);
});
gulp.task('build', function() {
    return gulp.src(SRC)
    .pipe(changed(DEST))
    .pipe(gulp.dest(DEST))
    .pipe(jscs({fix: true}))
    .pipe(jscs.reporter())
    .pipe(jscs.reporter('fail'))
    //.pipe(uglify())
    .pipe(rename({ extname: '.min.js' }))
    .pipe(gulp.dest(DEST));
})
gulp.task('default', ['clean:mobile']);