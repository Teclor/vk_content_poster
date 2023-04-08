import lib

try:
    posted_results = lib.VKPoster().post_batch(file_loader=lib.ImageLoader())
    print('Posted {} posts. Result:'.format(len(posted_results)))
    for res in posted_results:
        print(res)
except Exception as e:
    import traceback

    print('An error occurred while running a program:\n', traceback.format_exc())

