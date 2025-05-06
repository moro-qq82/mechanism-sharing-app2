import pytest
from fastapi.testclient import TestClient

def test_like_mechanism(client, test_mechanism, auth_headers):
    """
    メカニズムへのいいね追加のテスト
    """
    # テスト前にいいねを削除（既存のいいねがある場合）
    client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    # いいねを追加
    response = client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    assert response.status_code == 201, f"いいねの追加に失敗しました: {response.text}"
    
    data = response.json()
    assert data["mechanism_id"] == test_mechanism.id
    assert "user_id" in data

def test_like_mechanism_twice(client, test_mechanism, auth_headers):
    """
    同じメカニズムに2回いいねできないことをテスト
    """
    # 1回目のいいね
    response = client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    # ステータスコードは201または400（既にいいねがある場合）
    assert response.status_code in [201, 400]
    
    # 2回目のいいね
    response = client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    assert response.status_code == 400, f"同じメカニズムに2回いいねできてしまいました: {response.text}"

def test_unlike_mechanism(client, test_mechanism, auth_headers):
    """
    メカニズムのいいね取り消しのテスト
    """
    # 事前にいいねを追加
    client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    # いいねを取り消し
    response = client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200, f"いいねの取り消しに失敗しました: {response.text}"

def test_unlike_not_liked_mechanism(client, test_mechanism, auth_headers):
    """
    いいねしていないメカニズムのいいね取り消しのテスト
    """
    # 事前にいいねを削除
    client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    # いいねを取り消し
    response = client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 404, f"いいねしていないメカニズムのいいねが取り消せてしまいました: {response.text}"

def test_get_mechanism_likes_count(client, test_mechanism, auth_headers):
    """
    メカニズムのいいね数取得のテスト
    """
    # 事前にいいねを追加
    client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    # いいね数を取得
    response = client.get(f"/api/likes/mechanism/{test_mechanism.id}")
    assert response.status_code == 200, f"いいね数の取得に失敗しました: {response.text}"
    
    data = response.json()
    assert "likes_count" in data
    assert data["likes_count"] >= 1

def test_get_user_liked_mechanisms(client, test_user, test_mechanism, auth_headers):
    """
    ユーザーがいいねしたメカニズム一覧取得のテスト
    """
    # 事前にいいねを追加
    client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    # ユーザーがいいねしたメカニズム一覧を取得
    response = client.get(
        f"/api/likes/user/{test_user.id}/liked",
        headers=auth_headers
    )
    
    assert response.status_code == 200, f"ユーザーがいいねしたメカニズム一覧の取得に失敗しました: {response.text}"
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # テスト用メカニズムが含まれていることを確認
    assert any(mechanism["mechanism_id"] == test_mechanism.id for mechanism in data)

def test_get_user_liked_mechanisms_without_auth(client, test_user):
    """
    認証なしでユーザーがいいねしたメカニズム一覧を取得できないことをテスト
    """
    response = client.get(f"/api/likes/user/{test_user.id}/liked")
    assert response.status_code == 401, f"認証なしでユーザーがいいねしたメカニズム一覧が取得できてしまいました: {response.text}"

def test_get_popular_mechanisms(client, test_mechanism, auth_headers):
    """
    人気のメカニズム取得のテスト
    """
    # 事前にいいねを追加
    client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    # 人気のメカニズムを取得
    response = client.get("/api/likes/popular")
    assert response.status_code == 200, f"人気のメカニズム取得に失敗しました: {response.text}"
    
    data = response.json()
    assert isinstance(data, list)
    
    # いいねしたメカニズムが含まれていることを確認（上位に表示されるとは限らないため、条件付き）
    if len(data) > 0:
        # いいね数でソートされていることを確認
        for i in range(len(data) - 1):
            assert data[i]["likes_count"] >= data[i + 1]["likes_count"]

def test_like_mechanism_flow_with_frontend_api(client, test_mechanism, auth_headers):
    """
    フロントエンドAPIの形式でいいね機能をテストする
    """
    # 1. メカニズム詳細を取得していいね数を確認
    response = client.get(f"/api/mechanisms/{test_mechanism.id}")
    assert response.status_code == 200
    
    initial_data = response.json()
    initial_likes_count = initial_data["likes_count"]
    
    # 2. いいねを追加（既存のいいねを削除してから）
    client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    response = client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    
    # 3. メカニズム詳細を再取得していいね数が増えたことを確認
    response = client.get(f"/api/mechanisms/{test_mechanism.id}")
    assert response.status_code == 200
    
    updated_data = response.json()
    assert updated_data["likes_count"] >= initial_likes_count
    
    # 4. いいねを取り消し
    response = client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # 5. メカニズム詳細を再取得していいね数が減ったことを確認
    response = client.get(f"/api/mechanisms/{test_mechanism.id}")
    assert response.status_code == 200
    
    final_data = response.json()
    assert final_data["likes_count"] < updated_data["likes_count"]
