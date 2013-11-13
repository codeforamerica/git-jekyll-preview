require "./stats"


describe "Stats" do
  it "should return stats when passed a github url" do
    gh_stats = Stats.fetchGHStats("http://github.com/codeforamerica/cfa_coder_sounds")

    gh_stats["stars"].should.present?
  end
end
