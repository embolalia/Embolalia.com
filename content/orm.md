Title: On the new Willie ORM
Date: 2013-03-05 14:01:34

This is just a stream of consciousness brainstorm on the new ORM (database
abstrction) for [Willie](http://willie.dftba.net).

The DB should have the ability to execute SQL directly. Given the different
substitution strings between sqlite and MySQL's python bindings, this would
probably be best done with a wrapper method. My thought at the moment is just
to make an `execute` method which substitutes in the substitution string for
all of the %s'es in the query, sort of like what the rss module does now. This
might be worth including in 3.2, in case 4.0 takes forever to come out.

The primary use case that this database targets is retrieving information based
on a channel name or nick name. While a first glance makes it seem that channels
do *not* follow the IRC convention of `{}\` being upper-case `[]\`, nick names
do. This might make things more complicated, or less.

I don't know of a way to add a new equality test to a SQL database. It may be
possible, but especially since nicks and channels will likely still be in the
same column it would be difficult to do properly. I think the best way, then,
would be to have a mapping table of the "canonical" nick name - with the user's
preferred capitalization, perhaps updated when they're seen as a trigger rather
than referenced by someone else, to a "slug" which basically just lower-cases
per the IRC RFC. Channels, then, could be done the same way (though the slug
would not do the weird lower-case rule for channels). Other tables that want to
have nicks in them would have foreign keys to this table. Obviously this would
make things more complex, but then that's the point of an ORM.

The ORM should also include built-in support for what the bucket and rss modules
are already doing. The ability to join tables, and select from those joined
tables, is a must. Selections with `LIKE` are also necessary. At the same time,
though, deep knowledge of SQL *can not* be a requirement; in fact, requiring any
knowledge of SQL is to be avoided.
