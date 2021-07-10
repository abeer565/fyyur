def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #data = Venue.query.filter_by(id=venue_id).first()
  #return render_template('pages/show_venue.html', venue=data)
      ''' Getting a venue '''
      try:
        venue_result = Venue.query.get(venue_id)
        print(venue_result)
        if not venue_result:
            print('hii')
            return render_template('errors/404.html')
        #upcoming_shows_query = db.session.Show.join(Artist).filter(Show.Venues_id==venue_id).filter(Show.start_time>datetime.now()).all() 
        upcoming_shows_query = db.session.query(Show).join(Venue,Show.Venue_id==venue_id.id)
        # 
        print("the jiin")
        print(upcoming_shows_query)
        upcoming_shows = []
        for show in upcoming_shows_query:
          upcoming_shows.append({
              "artist_id": show.artist_id,
              "artist_name": show.artist.name,
               "artist_image_link": show.artist.image_link,
               #"start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
               "start_time":show['start_time']
            })
        past_shows_query = db.session.query(Show).join(Artist).filter(Show.Venues_id==venue_id).filter(Show.start_time<datetime.now()).all()      
        past_shows = []
        for show in past_shows_query:
           past_shows.append({
             "artist_id": show.artist_id,
              "artist_name": show.artist.name,
              "artist_image_link": show.artist.image_link,
              "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
            })


  for show in results_past_show_art:
      if (results_past_show_art.id == results_past_show_ven.id):
        past_shows.append({
        "artist_id": show.id,
        "artist_name": show.name,
        "artist_image_link": show.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
        return render_template('pages/show_venue.html', venue=data)
      except:
        flash('Record not found')
        return render_template('errors/404.html')

## art
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()

# ven
  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()

# mine ven 
  results_upcoming_show_art = db.session.query(Show, Artist).join(Artist).filter(Artist.show_id== Show.id).filter(Show.start_time>datetime.now()).all()
