/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

const gulp = require('gulp');
const typescript = require('gulp-typescript');
const sourcemaps = require('gulp-sourcemaps');
const terser = require('gulp-terser');
const postcss = require('gulp-postcss');
const cssnano = require('cssnano');
const autoprefixer = require('autoprefixer');
const browserSync = require('browser-sync').create();
const del = require('del');

// TypeScriptプロジェクトの設定
const tsProject = typescript.createProject('tsconfig.json');

// ビルドディレクトリのクリーン
function clean() {
    return del(['dist/**', '!dist']);
}

// TypeScriptのコンパイル
function compileTypescript() {
    return tsProject.src()
        .pipe(sourcemaps.init())
        .pipe(tsProject())
        .pipe(terser())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('dist'));
}

// CSSの処理
function styles() {
    return gulp.src('src/**/*.css')
        .pipe(sourcemaps.init())
        .pipe(postcss([
            autoprefixer(),
            cssnano()
        ]))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('dist'))
        .pipe(browserSync.stream());
}

// 静的ファイルのコピー
function copyStatic() {
    return gulp.src([
        'public/**/*',
        'src/**/*.html',
        'src/**/*.json',
        'src/**/*.svg',
        'src/**/*.png',
        'src/**/*.ico'
    ], { base: '.' })
    .pipe(gulp.dest('dist'));
}

// 開発サーバーの起動
function serve() {
    browserSync.init({
        server: {
            baseDir: './dist'
        },
        port: 3000
    });

    // ファイル変更の監視
    gulp.watch('src/**/*.ts', compileTypescript);
    gulp.watch('src/**/*.css', styles);
    gulp.watch([
        'public/**/*',
        'src/**/*.html',
        'src/**/*.json',
        'src/**/*.svg',
        'src/**/*.png',
        'src/**/*.ico'
    ], copyStatic);

    // ビルドファイルの変更を監視してブラウザをリロード
    gulp.watch('dist/**/*').on('change', browserSync.reload);
}

// ビルドタスク
const build = gulp.series(clean, gulp.parallel(compileTypescript, styles, copyStatic));

// 開発タスク
const dev = gulp.series(build, serve);

exports.clean = clean;
exports.build = build;
exports.dev = dev;
exports.default = dev;
