db = db.getSiblingDB("bookstore")

db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

db.authors.find()
db.books.find()

db.books.insertMany([
    { title: "The Great Gatsby", published_year: 1925, author_ids: "author_004" },
    { title: "To Kill a Mockingbird", published_year: 1960, author_ids: "author_005" }
])

db.authors.insertMany([
    {
        _id: 'author_004',
        name: 'F. Scott Fitzgerald',
        nationality: 'American',
        bio: [
            {
                short: 'American novelist, essayist, and short story writer.',
                long: 'F. Scott Fitzgerald was an American short-story writer and novelist famous for his depictions of the Jazz Age, a period in the 1920s characterized by prosperity, rapid social change, and a mood of exuberant optimism.'
            }
        ]
    },

    {
        _id: 'author_005',
        name: 'Harper Lee',
        nationality: 'American',
        bio: [
            {
                short: 'American novelist, essayist, and short story writer.',
                long: 'F. Scott Fitzgerald was an American short-story writer and novelist famous for his depictions of the Jazz Age, a period in the 1920s characterized by prosperity, rapid social change, and a mood of exuberant optimism.'
            }
        ]
    }
])

db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })