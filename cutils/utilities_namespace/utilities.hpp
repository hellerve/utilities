namespace utilities {

    template <typename F, typename ...Args>
    auto async(F&& f, Args&&... args) -> std::future<typename std::result_of<F (Args...)>::type>{
        using result_type = typename std::result_of<F (Args...)>::type;
        using packaged_type = std::packaged_task<result_type()>;

        auto p = new packaged_type(std::forward<F>(f), std::forward<Args>(args)...);
        auto res = p->get_future();

        dispatch_async_f(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), p,
                         [](void* f_){
                            packaged_type* f = static_cast<packaged_type*>(f_);
                            (*f)();
                            delete f;
                         });

        return res;
    }
}
