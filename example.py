import gmapslivepopulartimes

magic_pb_param = "!1m18!1s0x0:0x39acbe41c4eec73f!3m12!1m3!1d229292.2503210766!2d-97.87335716400854!3d30.331380841649835!2m3!1f0!2f0!3f0!3m2!1i920!2i799!4f13.1!4m2!3d30.323359769150866!4d-97.73918151855469!5e4!6storchy's tacos!12m3!2m2!1i392!2i106!13m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i200!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e4!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!2b1!4b1!9b0!14m5!1sflbFWaORNouQ0gKQ97-gBA!4m1!2i5357!7e81!12e3!15m17!1m1!4e2!2b1!5m4!2b1!3b1!5b1!6b1!10m1!8e3!17b1!24b1!25b1!26b1!30m1!2b1!36b1!21m28!1m6!1m2!1i0!2i0!2m2!1i458!2i799!1m6!1m2!1i870!2i0!2m2!1i920!2i799!1m6!1m2!1i0!2i0!2m2!1i920!2i20!1m6!1m2!1i0!2i779!2m2!1i920!2i799!22m1!1e81!29m0!30m1!3b1"

place = gmapslivepopulartimes.LivePop(magic_pb_param)

place = place.get_live_data()

print(place.status)
# 'Place has live popularity data'

print(place.livePop)
# 97

print(place.historical_popular_value())
# 84

print(place.liveDesc)
# 'As busy as it gets'